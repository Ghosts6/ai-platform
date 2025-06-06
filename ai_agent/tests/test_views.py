import pytest
import json
from unittest.mock import patch, MagicMock
from django.test import Client
from agent.agent_manager import AgentRouter

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def router():
    echo_agent = MagicMock()
    echo_agent.handle.return_value = "Echoed"
    summarizer_agent = MagicMock()
    summarizer_agent.handle.return_value = "Summarized"

    router = AgentRouter()
    router.agents = {
        "echo": echo_agent,
        "summarize": summarizer_agent,
    }
    router.routing_rules = [
        (["summarize", "summary"], summarizer_agent),
    ]
    return router, echo_agent, summarizer_agent

@pytest.mark.django_db
@patch('agent.agent_manager.AgentLog.objects.create')
def test_agent_router_routes_correctly(mock_log_create, router):
    router_instance, echo_agent, summarizer_agent = router

    # Test summarizer route
    res = router_instance.route("Please summarize this text")
    summarizer_agent.handle.assert_called_once_with("Please summarize this text")
    assert res == "Summarized"
    mock_log_create.assert_called()

    # Test fallback echo route
    res = router_instance.route("Hello world")
    echo_agent.handle.assert_called_once_with("Hello world")
    assert res == "Echoed"
    mock_log_create.assert_called()

@pytest.mark.parametrize("prompt, expected_start", [
    ("Hello", "Echo:"),
    ("Can you summarize this text?", "Summary:")
])
@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
@patch('agent.agent_manager.AgentLog.objects.create')
def test_agent_response(mock_log_create, mock_chat_create, client, prompt, expected_start):
    # Mock OpenAI response for summarizer
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'This is a mocked summary.'})]
    mock_chat_create.return_value = mock_response
    mock_log_create.return_value = None

    res = client.post(
        '/api/agent/respond/',
        data=json.dumps({'prompt': prompt}),
        content_type='application/json'
    )
    assert res.status_code == 200
    assert res.json()['response'].startswith(expected_start)

@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
@patch('agent.agent_manager.AgentLog.objects.create')
def test_agent_summarizer_response(mock_log_create, mock_chat_create, client):
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'This is a mocked summary.'})]
    mock_chat_create.return_value = mock_response
    mock_log_create.return_value = None

    res = client.post(
        '/api/agent/respond/',
        data=json.dumps({'prompt': 'Can you summarize this text?'}),
        content_type='application/json'
    )
    assert res.status_code == 200
    assert "Summary:" in res.json()['response']
    assert "mocked summary" in res.json()['response'].lower()
