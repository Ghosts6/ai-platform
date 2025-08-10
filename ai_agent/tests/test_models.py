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

@pytest.mark.django_db
@patch('core_services.agents.email.openai.chat.completions.create')
def test_email_agent_tools(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'This is a reply.'})]
    mock_create.return_value = mock_response
    agent = EmailAgent(agent_id="email", name="email")
    result = asyncio.run(agent.process({"prompt": "suggest reply to this email: ..."}))
    assert "EmailAgent:" in result['result']
    result2 = asyncio.run(agent.process({"prompt": "summarize this email: ..."}))
    assert "EmailAgent:" in result2['result']

@pytest.mark.django_db
@patch('core_services.agents.excel.openai.chat.completions.create')
def test_excel_agent_tools(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'SUM(A1:A10)'})]
    mock_create.return_value = mock_response
    agent = ExcelAgent(agent_id="excel", name="excel")
    result = asyncio.run(agent.process({"prompt": "suggest formula to sum column A"}))
    assert "ExcelAgent:" in result['result']
    result2 = asyncio.run(agent.process({"prompt": "summarize this table: ..."}))
    assert "ExcelAgent:" in result2['result']

@pytest.mark.django_db
@patch('core_services.agents.summarize.openai.chat.completions.create')
@patch('core_services.agents.qa.openai.chat.completions.create')
@patch('core_services.agents.email.openai.chat.completions.create')
@patch('core_services.agents.excel.openai.chat.completions.create')
def test_agent_router_selection(mock_excel, mock_email, mock_qa, mock_summarize):
    # Setup mocks
    mock_excel.return_value = MagicMock(choices=[MagicMock(message={'content': 'Excel result'})])
    mock_email.return_value = MagicMock(choices=[MagicMock(message={'content': 'Email result'})])
    mock_qa.return_value = MagicMock(choices=[MagicMock(message={'content': 'QA result'})])
    mock_summarize.return_value = MagicMock(choices=[MagicMock(message={'content': 'Summary result'})])
    router = AgentRouter()
    assert "ExcelAgent:" in asyncio.run(router.route("suggest formula to sum column A"))
    assert "EmailAgent:" in asyncio.run(router.route("suggest reply to this email: ..."))
    assert "Summary:" in asyncio.run(router.route("summarize this text"))
    assert "Answer:" in asyncio.run(router.route("What is the capital of France?"))
