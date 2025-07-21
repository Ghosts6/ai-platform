import pytest
import json
from unittest.mock import patch, MagicMock
from django.test import Client
from agent.agent_manager import AgentRouter
from django.apps import apps
ContactMessage = apps.get_model('core_services', 'ContactMessage')
from core_services.models import ChatSession, ChatMessage
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
@patch('core_services.agents.qa.openai.chat.completions.create')
@patch('core_services.agents.email.openai.chat.completions.create')
@patch('core_services.agents.excel.openai.chat.completions.create')
def test_agent_respond_view(mock_excel, mock_email, mock_qa, mock_summarize, client):
    mock_excel.return_value = MagicMock(choices=[MagicMock(message={'content': 'Excel result'})])
    mock_email.return_value = MagicMock(choices=[MagicMock(message={'content': 'Email result'})])
    mock_qa.return_value = MagicMock(choices=[MagicMock(message={'content': 'QA result'})])
    mock_summarize.return_value = MagicMock(choices=[MagicMock(message={'content': 'Summary result'})])

    # Excel
    res = client.post('/api/agent/respond/', data=json.dumps({'prompt': 'suggest formula to sum column A'}), content_type='application/json')
    assert res.status_code == 200
    assert "ExcelAgent:" in res.json()['response']
    # Email
    res = client.post('/api/agent/respond/', data=json.dumps({'prompt': 'suggest reply to this email: ...'}), content_type='application/json')
    assert res.status_code == 200
    assert "EmailAgent:" in res.json()['response']
    # Summarize
    res = client.post('/api/agent/respond/', data=json.dumps({'prompt': 'summarize this text'}), content_type='application/json')
    assert res.status_code == 200
    assert "Summary:" in res.json()['response']
    # QA
    res = client.post('/api/agent/respond/', data=json.dumps({'prompt': 'What is the capital of France?'}), content_type='application/json')
    assert res.status_code == 200
    assert "Answer:" in res.json()['response']

@pytest.mark.parametrize("prompt, expected_start", [
    ("What is the capital of France?", "Answer:"),
    ("summarize this text", "Summary:"),
    ("suggest reply to this email: ...", "EmailAgent:"),
    ("suggest formula to sum column A", "ExcelAgent:")
])
@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
@patch('core_services.agents.qa.openai.chat.completions.create')
@patch('core_services.agents.email.openai.chat.completions.create')
@patch('core_services.agents.excel.openai.chat.completions.create')
def test_agent_response(mock_excel, mock_email, mock_qa, mock_summarize, client, prompt, expected_start):
    mock_excel.return_value = MagicMock(choices=[MagicMock(message={'content': 'Excel result'})])
    mock_email.return_value = MagicMock(choices=[MagicMock(message={'content': 'Email result'})])
    mock_qa.return_value = MagicMock(choices=[MagicMock(message={'content': 'QA result'})])
    mock_summarize.return_value = MagicMock(choices=[MagicMock(message={'content': 'Summary result'})])

    res = client.post(
        '/api/agent/respond/',
        data=json.dumps({'prompt': prompt}),
        content_type='application/json'
    )
    assert res.status_code == 200
    assert res.json()['response'].startswith(expected_start)

@pytest.mark.django_db
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

@pytest.mark.django_db
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

@pytest.mark.django_db
def test_chat_history_view():
    user = User.objects.create_user(username='testuser', password='testpass')
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

@pytest.mark.django_db
def test_chat_session_view():
    user = User.objects.create_user(username='testuser', password='testpass')
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

@pytest.mark.django_db
def test_last_chat_session_view():
    user = User.objects.create_user(username='testuser', password='testpass')
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
