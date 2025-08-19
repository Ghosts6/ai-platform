import pytest
from core_services.models import AgentLog, AgentMemory
from django.utils import timezone
from agent.agent_manager import AgentRouter
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.agents.summarize import SummarizerAgent
from core_services.agents.qa import QAPairAgent
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
def test_agentlog_creation():
    log = AgentLog.objects.create(
        agent_name="test_agent",
        prompt="Test prompt",
        response="Test response",
        created_at=timezone.now()
    )
    assert log.pk is not None
    assert log.agent_name == "test_agent"
    assert log.prompt == "Test prompt"
    assert log.response == "Test response"
    assert isinstance(log.created_at, timezone.datetime)

@pytest.mark.django_db
def test_agentmemory_crud():
    AgentMemory.objects.create(agent_name="test", key="foo", value="bar")
    mem = AgentMemory.objects.get(agent_name="test", key="foo")
    assert mem.value == "bar"
    mem.value = "baz"
    mem.save()
    assert AgentMemory.objects.get(agent_name="test", key="foo").value == "baz"
    AgentMemory.objects.filter(agent_name="test", key="foo").delete()
    assert AgentMemory.objects.filter(agent_name="test", key="foo").count() == 0

import asyncio

@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
def test_summarizer_agent_openai(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'This is a summary.'})]
    mock_create.return_value = mock_response
    agent = SummarizerAgent(agent_id="summarize", name="summarize")
    result = asyncio.run(agent.process({"prompt": "summarize this text"}))
    assert "Summary:" in result['result']

@pytest.mark.django_db
@patch('core_services.agents.qa.openai.chat.completions.create')
def test_qa_agent_openai(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'Paris'})]
    mock_create.return_value = mock_response
    agent = QAPairAgent(agent_id="qa", name="qa")
    result = asyncio.run(agent.process({"prompt": "What is the capital of France?"}))
    assert "Answer:" in result['result']
    # Should be stored in memory
    mem = AgentMemory.objects.get(agent_name="qa", key="What is the capital of France?")
    assert mem.value == "Paris"


