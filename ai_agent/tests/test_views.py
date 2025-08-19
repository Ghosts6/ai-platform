import pytest
import json
from unittest.mock import patch, MagicMock
from django.test import Client
from django.apps import apps
ContactMessage = apps.get_model('core_services', 'ContactMessage')
from core_services.models import ChatSession, ChatMessage
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async
from django.urls import reverse
from profiles.models import O365Token
import datetime
import asyncio
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.agents.calendar import CalendarAgent
from core_services.agents.teams import TeamsAgent

@pytest.mark.django_db(transaction=True)
def test_contact_message_human(client):
    data = {
        'name': 'Alice',
        'email': 'alice@example.com',
        'message': 'Hello, this is a test.',
        'website': ''  # honeypot empty
    }
    res = client.post('/api/core/contact/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    assert res.json()['message'] == 'Your message has been sent successfully!'
    assert ContactMessage.objects.filter(email='alice@example.com').exists()

@pytest.mark.django_db(transaction=True)
def test_contact_message_bot(client):
    data = {
        'name': 'Bot',
        'email': 'bot@example.com',
        'message': 'Spam message',
        'website': 'spammy'  # honeypot filled
    }
    res = client.post('/api/core/contact/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 200
    assert res.json()['message'] == 'Bot detected.'
    assert not ContactMessage.objects.filter(email='bot@example.com').exists()

@pytest.mark.django_db(transaction=True)
def test_chat_history_view(user):
    session1 = ChatSession.objects.create(user=user)
    session2 = ChatSession.objects.create(user=user)
    ChatMessage.objects.create(session=session1, sender='user', text='Hello')
    ChatMessage.objects.create(session=session1, sender='agent', text='Hi!')
    ChatMessage.objects.create(session=session2, sender='user', text='Another chat')
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get('/api/core/chat/history/')
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]['id'] == session2.id  # Most recent first
    assert res.json()[1]['id'] == session1.id

@pytest.mark.django_db(transaction=True)
def test_chat_session_view(user):
    session = ChatSession.objects.create(user=user)
    ChatMessage.objects.create(session=session, sender='user', text='Hello')
    ChatMessage.objects.create(session=session, sender='agent', text='Hi!')
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get(f'/api/core/chat/session/{session.id}/')
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]['sender'] == 'user'
    assert res.json()[1]['sender'] == 'agent'
    # Test not found
    res2 = client.get(f'/api/core/chat/session/9999/')
    assert res2.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_last_chat_session_view(user):
    session1 = ChatSession.objects.create(user=user)
    session2 = ChatSession.objects.create(user=user)
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get('/api/core/chat/last/')
    assert res.status_code == 200
    assert res.json()['id'] == session2.id
    # Test no session
    user2 = User.objects.create_user(username='emptyuser', password='testpass')
    client.force_authenticate(user=user2)
    res2 = client.get('/api/core/chat/last/')
    assert res2.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_respond_to_prompt_authenticated(user):
    """
    Test the respond_to_prompt view with an authenticated user.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )
    
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    with patch('agent.views.router.route') as mock_route:
        async def async_mock_route(*args, **kwargs):
            return "Test response"
        mock_route.side_effect = async_mock_route
        
        response = client.post(
            reverse('respond_to_prompt'),
            {'prompt': 'test prompt'},
            format='json'
        )
        
        assert response.status_code == 200
        assert response.json()['response'] == 'Test response'

@pytest.mark.django_db(transaction=True)
def test_respond_to_prompt_unauthenticated(user):
    """
    Test the respond_to_prompt view with an unauthenticated user.
    """
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    with patch('agent.views.router.route') as mock_route:
        async def async_mock_route(*args, **kwargs):
            return "EmailAgent: Please authenticate with Microsoft to use email features. You can do so by visiting /ms_auth/login"
        mock_route.side_effect = async_mock_route
        
        response = client.post(
            reverse('respond_to_prompt'),
            {'prompt': 'check my email'},
            format='json'
        )
        
        assert response.status_code == 200
        assert "Please authenticate with Microsoft" in response.json()['response']

@pytest.mark.django_db(transaction=True)
def test_email_agent_authenticated(user):
    """
    Test that the EmailAgent is authenticated if a valid token exists.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.email.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = EmailAgent(agent_id='email', name='email', user=user)
        
        assert agent.account is not None

@pytest.mark.django_db(transaction=True)
def test_email_agent_process_authenticated(user):
    """
    Test the process method of an authenticated EmailAgent.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.email.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        mock_mailbox = MagicMock()
        mock_instance.mailbox.return_value = mock_mailbox
        mock_inbox = MagicMock()
        mock_mailbox.inbox_folder.return_value = mock_inbox
        mock_inbox.unread_count = 5

        agent = EmailAgent(agent_id='email', name='email', user=user)
        result = asyncio.run(agent.process(task={'prompt': 'check for unread emails'}))

        assert result['result'] == 'EmailAgent: You have 5 unread emails.'

@pytest.mark.django_db(transaction=True)
def test_email_agent_process_unauthenticated(user):
    """
    Test the process method of an unauthenticated EmailAgent.
    """
    agent = EmailAgent(agent_id='email', name='email', user=user)
    result = asyncio.run(agent.process(task={'prompt': 'check for unread emails'}))

    assert "Please authenticate with Microsoft" in result['result']

@pytest.mark.django_db(transaction=True)
def test_excel_agent_authenticated(user):
    """
    Test that the ExcelAgent is authenticated if a valid token exists.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.excel.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = ExcelAgent(agent_id='excel', name='excel', user=user)
        
        assert agent.account is not None

@pytest.mark.django_db(transaction=True)
def test_excel_agent_process_authenticated(user):
    """
    Test the process method of an authenticated ExcelAgent.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.excel.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        mock_storage = MagicMock()
        mock_instance.storage.return_value = mock_storage
        mock_drive = MagicMock()
        mock_storage.get_default_drive.return_value = mock_drive
        mock_root = MagicMock()
        mock_drive.get_root_folder.return_value = mock_root
        mock_item = MagicMock()
        mock_item.name = 'test_file.xlsx'
        mock_root.get_items.return_value = [mock_item]


        agent = ExcelAgent(agent_id='excel', name='excel', user=user)
        result = asyncio.run(agent.process(task={'prompt': 'list my files in onedrive'}))

        assert "test_file.xlsx" in result['result']

@pytest.mark.django_db(transaction=True)
def test_calendar_agent_authenticated(user):
    """
    Test that the CalendarAgent is authenticated if a valid token exists.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.calendar.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = CalendarAgent(agent_id='calendar', name='calendar', user=user)
        
        assert agent.account is not None

@pytest.mark.django_db(transaction=True)
def test_calendar_agent_process_authenticated(user):
    """
    Test the process method of an authenticated CalendarAgent.
    """
    O365Token.objects.create(
        user=user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('core_services.agents.calendar.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        mock_schedule = MagicMock()
        mock_instance.schedule.return_value = mock_schedule
        mock_calendar = MagicMock()
        mock_schedule.get_default_calendar.return_value = mock_calendar
        mock_event = MagicMock()
        mock_event.subject = 'Test Event'
        mock_event.start = datetime.datetime.now(datetime.timezone.utc)
        mock_calendar.get_events.return_value = [mock_event]


        agent = CalendarAgent(agent_id='calendar', name='calendar', user=user)
        result = asyncio.run(agent.process(task={'prompt': 'list my events'}))

        assert "Test Event" in result['result']

@pytest.mark.django_db
def test_teams_agent_creates_event(monkeypatch):
    # Mock O365 Account and Calendar
    class DummyEvent:
        def __init__(self):
            self.subject = None
            self.start = None
            self.end = None
            self.location = None
            self.body = None
            self.saved = False
        def save(self):
            self.saved = True
    class DummyCalendar:
        def new_event(self):
            return DummyEvent()
    class DummySchedule:
        def get_default_calendar(self):
            return DummyCalendar()
    class DummyAccount:
        is_authenticated = True
        def schedule(self):
            return DummySchedule()
    monkeypatch.setattr("core_services.agents.teams.Account", lambda *a, **kw: DummyAccount())
    agent = TeamsAgent(agent_id="teams", name="teams")
    result = asyncio.run(agent.process({"prompt": "maintenance window on Friday"}))
    assert "Created calendar event" in result['result']

@pytest.mark.django_db
def test_teams_agent_no_action(monkeypatch):
    class DummyAccount:
        is_authenticated = True
        def schedule(self):
            class DummySchedule:
                def get_default_calendar(self):
                    class DummyCalendar:
                        def new_event(self):
                            class DummyEvent:
                                def save(self): pass
                            return DummyEvent()
                    return DummyCalendar()
            return DummySchedule()
    monkeypatch.setattr("core_services.agents.teams.Account", lambda *a, **kw: DummyAccount())
    agent = TeamsAgent(agent_id="teams", name="teams")
    result = asyncio.run(agent.process({"prompt": "random unrelated prompt"}))
    assert "No relevant action" in result['result']
