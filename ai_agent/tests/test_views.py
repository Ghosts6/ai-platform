import pytest
import json
from unittest.mock import patch, MagicMock
from django.test import Client
from agent.agent_manager import AgentRouter
from django.apps import apps
ContactMessage = apps.get_model('core_services', 'ContactMessage')

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
