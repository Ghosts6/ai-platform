import pytest
import json
import uuid
from unittest.mock import patch, MagicMock
from django.test import Client
from django.apps import apps
ContactMessage = apps.get_model('core_services', 'ContactMessage')
from ai_agent.core_services.models import ChatSession, ChatMessage, Agent
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async
from django.urls import reverse
from ai_agent.profiles.models import O365Token
import datetime
import asyncio
from ai_agent.core_services.agents.email import EmailAgent
from ai_agent.core_services.agents.excel import ExcelAgent
from ai_agent.core_services.agents.calendar import CalendarAgent
from ai_agent.core_services.agents.teams import TeamsAgent

import io
import os
import tempfile
import pandas as pd

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

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
def test_chat_history_view(test_user):
    session1 = ChatSession.objects.create(user=test_user)
    session2 = ChatSession.objects.create(user=test_user)
    ChatMessage.objects.create(session=session1, sender='user', text='Hello')
    ChatMessage.objects.create(session=session1, sender='agent', text='Hi!')
    ChatMessage.objects.create(session=session2, sender='user', text='Another chat')
    client = APIClient()
    client.force_authenticate(user=test_user)
    res = client.get('/api/core/chat/history/')
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]['id'] == str(session2.id)  # Most recent first
    assert res.json()[1]['id'] == str(session1.id)

@pytest.mark.django_db(transaction=True)
def test_chat_session_view(test_user):
    session = ChatSession.objects.create(user=test_user)
    ChatMessage.objects.create(session=session, sender='user', text='Hello')
    ChatMessage.objects.create(session=session, sender='agent', text='Hi!')
    client = APIClient()
    client.force_authenticate(user=test_user)
    res = client.get(f'/api/core/chat/session/{session.id}/')
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]['sender'] == 'user'
    assert res.json()[1]['sender'] == 'agent'
    # Test not found
    res2 = client.get(f'/api/core/chat/session/{uuid.uuid4()}/')
    assert res2.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_last_chat_session_view(test_user):
    session1 = ChatSession.objects.create(user=test_user)
    session2 = ChatSession.objects.create(user=test_user)
    client = APIClient()
    client.force_authenticate(user=test_user)
    res = client.get('/api/core/chat/last/')
    assert res.status_code == 200
    assert res.json()['id'] == str(session2.id)
    # Test no session
    user2 = User.objects.create_user(username='emptyuser', password='testpass')
    client.force_authenticate(user=user2)
    res2 = client.get('/api/core/chat/last/')
    assert res2.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_respond_to_prompt_unauthenticated(client):
    response = client.post(
        reverse('respond_to_prompt'),
        {'prompt': 'test prompt'},
        format='json'
    )
    assert response.status_code == 401

@pytest.mark.django_db(transaction=True)
@patch('ai_agent.agent.agent_manager.AgentRouter.route')
def test_respond_to_prompt_authenticated(mock_route, test_user):
    mock_route.return_value = "Test response"
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = client.post(
        reverse('respond_to_prompt'),
        {'prompt': 'test prompt'},
        format='json'
    )
    
    assert response.status_code == 200
    assert response.json()['response'] == 'Test response'
    mock_route.assert_called_once()

@pytest.mark.django_db(transaction=True)
def test_email_agent_authenticated(test_user):
    agent_model = Agent.objects.create(name="email", agent_type="email", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('ai_agent.core_services.agents.email.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = EmailAgent(agent_instance=agent_model, user=test_user)
        account = asyncio.run(agent._get_account())
        assert account is not None

@pytest.mark.django_db(transaction=True)
def test_email_agent_process_authenticated(test_user):
    agent_model = Agent.objects.create(name="email", agent_type="email", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('ai_agent.core_services.agents.email.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        mock_mailbox = MagicMock()
        mock_instance.mailbox.return_value = mock_mailbox
        mock_inbox = MagicMock()
        mock_mailbox.inbox_folder.return_value = mock_inbox
        mock_inbox.unread_count = 5

        agent = EmailAgent(agent_instance=agent_model, user=test_user)
        result = asyncio.run(agent.process(task={'prompt': 'check for unread emails'}))

        assert result['result'] == 'EmailAgent: You have 5 unread emails.'

@pytest.mark.django_db(transaction=True)
def test_email_agent_process_unauthenticated(test_user):
    agent_model = Agent.objects.create(name="email", agent_type="email", created_by=test_user)
    agent = EmailAgent(agent_instance=agent_model, user=test_user)
    result = asyncio.run(agent.process(task={'prompt': 'check for unread emails'}))

    assert "Please authenticate with Microsoft" in result['result']

@pytest.mark.django_db(transaction=True)
def test_excel_agent_authenticated(test_user):
    agent_model = Agent.objects.create(name="excel", agent_type="excel", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('ai_agent.core_services.agents.excel.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = ExcelAgent(agent_instance=agent_model, user=test_user)
        asyncio.run(agent._ensure_account())
        assert agent.account is not None

@pytest.mark.django_db(transaction=True)
@patch('ai_agent.core_services.agents.excel.Account')
def test_excel_agent_process_authenticated(mock_account, test_user):
    agent_model = Agent.objects.create(name="excel", agent_type="excel", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )
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

    agent = ExcelAgent(agent_instance=agent_model, user=test_user)
    result = asyncio.run(agent.process(task={'prompt': 'list my files in onedrive'}))

    assert "test_file.xlsx" in result['result']

@pytest.mark.django_db(transaction=True)
def test_calendar_agent_authenticated(test_user):
    agent_model = Agent.objects.create(name="calendar", agent_type="calendar", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )

    with patch('ai_agent.core_services.agents.calendar.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.is_authenticated = True
        
        agent = CalendarAgent(agent_instance=agent_model, user=test_user)
        account = asyncio.run(agent._get_account())
        assert account is not None

@pytest.mark.django_db(transaction=True)
@patch('ai_agent.core_services.agents.calendar.Account')
def test_calendar_agent_process_authenticated(mock_account, test_user):
    agent_model = Agent.objects.create(name="calendar", agent_type="calendar", created_by=test_user)
    O365Token.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    )
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

    agent = CalendarAgent(agent_instance=agent_model, user=test_user)
    result = asyncio.run(agent.process(task={'prompt': 'list my events'}))

    assert "Test Event" in result['result']

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.teams.TeamsAgent._get_account')
async def test_teams_agent_creates_event(mock_get_account, test_user):
    agent_model = await sync_to_async(Agent.objects.create)(name="teams", agent_type="teams", created_by=test_user)
    
    mock_account = MagicMock()
    mock_account.is_authenticated = True
    mock_schedule = MagicMock()
    mock_account.schedule.return_value = mock_schedule
    mock_calendar = MagicMock()
    mock_schedule.get_default_calendar.return_value = mock_calendar
    mock_event = MagicMock()
    mock_calendar.new_event.return_value = mock_event
    
    mock_get_account.return_value = mock_account
    
    agent = TeamsAgent(agent_instance=agent_model, user=test_user)
    result = await agent.process({"prompt": "maintenance window on Friday"})
    assert "Created calendar event" in result['result']

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.teams.TeamsAgent._get_account')
async def test_teams_agent_no_action(mock_get_account, test_user):
    agent_model = await sync_to_async(Agent.objects.create)(name="teams", agent_type="teams", created_by=test_user)
    
    mock_account = MagicMock()
    mock_account.is_authenticated = True
    mock_get_account.return_value = mock_account
    
    agent = TeamsAgent(agent_instance=agent_model, user=test_user)
    result = await agent.process({"prompt": "random unrelated prompt"})
    assert "No relevant action triggered" in result['result']


@pytest.mark.django_db(transaction=True)
def test_chat_history_requires_auth(client):
    url = "/api/core/chat/history/"
    res = client.get(url)
    assert res.status_code in (401, 403)


@pytest.mark.django_db(transaction=True)
def test_chat_session_requires_auth(client):
    url = f"/api/core/chat/session/{uuid.uuid4()}/"
    res = client.get(url)
    assert res.status_code in (401, 403)


@pytest.mark.django_db(transaction=True)
def test_agent_respond_excel_describe_with_csv(client, test_user):
    Agent.objects.create(name="excel", agent_type="excel", created_by=test_user)
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    tmp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(tmp_dir, "test_data.csv")
    df.to_csv(csv_path, index=False)

    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    with open(csv_path, 'rb') as f:
        url = "/api/agent/respond/"
        data = {
            'prompt': 'describe',
            'agent': 'excel',
            'file': f,
        }
        res = client.post(url, data)
    assert res.status_code == 200, res.content
    payload = res.json()
    assert 'response' in payload
    assert 'ExcelAgent' in payload['response']['result']
    assert 'describe' in payload['response']['result'].lower() or 'description' in payload['response']['result'].lower()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.excel.openai.OpenAI')
async def test_excel_agent_summarize_fallback_without_openai_key(mock_openai_client, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="excel", defaults={"agent_type": "excel", "created_by": test_user})
    # Configure the mock to not raise an error when instantiated
    mock_openai_client.return_value = MagicMock()
    mock_openai_client.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='Mock summary'))]
    )

    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']

    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Email": ["a@example.com", "b@example.com"]})
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".csv")
    os.close(tmp_fd)
    df.to_csv(tmp_path, index=False)

    try:
        agent = ExcelAgent(agent_instance=agent_model, user=test_user, file_path=tmp_path)
        result = await agent.process(task={'prompt': 'summarize this file'})
        # Since API key is not set, it should fallback to local processing,
        # or if the prompt is specific enough, it might try LLM and fail gracefully
        assert 'Columns' in result['result'] or 'Mock summary' in result['result']
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


@pytest.mark.django_db(transaction=True)
def test_chat_session_delete_success(test_user):
    """
    Tests that a user can successfully delete their own chat session.
    """
    session = ChatSession.objects.create(user=test_user)
    session_id = session.id
    client = APIClient()
    client.force_authenticate(user=test_user)
    
    assert ChatSession.objects.filter(id=session_id).exists()
    
    res = client.delete(f'/api/core/chat/session/{session_id}/delete/')
    
    assert res.status_code == 204
    assert not ChatSession.objects.filter(id=session_id).exists()

@pytest.mark.django_db(transaction=True)
def test_chat_session_delete_unauthorized(test_user):
    """
    Tests that a user cannot delete a chat session belonging to another user.
    """
    other_user = User.objects.create_user(username='otheruser', password='password')
    session = ChatSession.objects.create(user=other_user)
    session_id = session.id
    
    client = APIClient()
    client.force_authenticate(user=test_user)
    
    res = client.delete(f'/api/core/chat/session/{session_id}/delete/')
    
    # The view returns 404 for both "not found" and "not authorized"
    assert res.status_code == 404
    assert ChatSession.objects.filter(id=session_id).exists()

