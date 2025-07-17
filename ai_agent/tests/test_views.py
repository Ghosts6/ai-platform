import pytest
import json
from unittest.mock import patch, MagicMock
from django.test import Client
from agent.agent_manager import AgentRouter
from django.apps import apps
ContactMessage = apps.get_model('core_services', 'ContactMessage')
User = apps.get_model('auth', 'User')

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
def test_register_human(client):
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'Testpass123',
        'website': ''
    }
    res = client.post('/api/profiles/register/', data=json.dumps(data), content_type='application/json')
    assert res.status_code in (201, 200)
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_register_bot(client):
    data = {
        'username': 'botuser',
        'email': 'botuser@example.com',
        'password': 'Testpass123',
        'website': 'spammy'
    }
    res = client.post('/api/profiles/register/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    assert 'website' in res.json()
    assert not User.objects.filter(username='botuser').exists()

@pytest.mark.django_db
def test_login_human(client):
    User.objects.create_user(username='loginuser', email='loginuser@example.com', password='Testpass123')
    data = {
        'username': 'loginuser',
        'password': 'Testpass123',
        'website': ''
    }
    res = client.post('/api/profiles/login/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 200
    assert 'token' in res.json()

@pytest.mark.django_db
def test_login_bot(client):
    User.objects.create_user(username='botlogin', email='botlogin@example.com', password='Testpass123')
    data = {
        'username': 'botlogin',
        'password': 'Testpass123',
        'website': 'spammy'
    }
    res = client.post('/api/profiles/login/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    assert res.json()['error'] == 'Bot detected.'

@pytest.mark.django_db
def test_password_reset_request_human(client):
    User.objects.create_user(username='resetuser', email='resetuser@example.com', password='Testpass123')
    data = {
        'email': 'resetuser@example.com',
        'website': ''
    }
    res = client.post('/api/profiles/password-reset/', data=json.dumps(data), content_type='application/json')
    assert res.status_code in (200, 201)
    assert 'detail' in res.json() or 'status' in res.json() or 'success' in res.json() or 'message' in res.json()

@pytest.mark.django_db
def test_password_reset_request_bot(client):
    User.objects.create_user(username='resetbot', email='resetbot@example.com', password='Testpass123')
    data = {
        'email': 'resetbot@example.com',
        'website': 'spammy'
    }
    res = client.post('/api/profiles/password-reset/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    assert res.json()['error'] == 'Bot detected.'

@pytest.mark.django_db
def test_password_reset_confirm_bot(client):
    data = {
        'token': 'dummy-token',
        'password': 'Newpass123',
        'website': 'spammy'
    }
    res = client.post('/api/profiles/password-reset/confirm/', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    assert res.json()['error'] == 'Bot detected.'
