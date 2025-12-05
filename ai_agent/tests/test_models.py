import pytest
from ai_agent.core_services.models import AgentLog, AgentMemory
from django.utils import timezone
from ai_agent.agent.agent_manager import AgentRouter
from ai_agent.core_services.agents.email import EmailAgent
from ai_agent.core_services.agents.excel import ExcelAgent
from ai_agent.core_services.agents.summarize import SummarizerAgent
from ai_agent.core_services.agents.qa import QAPairAgent
from unittest.mock import patch, MagicMock
from freezegun import freeze_time
from ai_agent.profiles.models import O365Token
import datetime

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
@patch('ai_agent.core_services.agents.summarize.openai.chat.completions.create')
def test_summarizer_agent_openai(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'This is a summary.'})]
    mock_create.return_value = mock_response
    agent = SummarizerAgent(agent_id="summarize", name="summarize")
    result = asyncio.run(agent.process({"prompt": "summarize this text"}))
    assert "Summary:" in result['result']

@pytest.mark.django_db
@patch('ai_agent.core_services.agents.qa.openai.chat.completions.create')
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
def test_agent_router_initialization():
    router = AgentRouter()
    assert "summarize" in router.agent_classes
    assert "qa" in router.agent_classes
    assert "email" in router.agent_classes
    assert "excel" in router.agent_classes
    assert "teams" in router.agent_classes
    assert "calendar" in router.agent_classes
    assert len(router.routing_rules) > 0



@pytest.mark.django_db
@patch('ai_agent.core_services.agents.excel.ExcelAgent._process_local_file')
def test_excel_agent_process_local_file_called(mock_process_local_file, user):
    mock_process_local_file.return_value = {"result": "processed"}
    agent = ExcelAgent(agent_id="excel", name="excel", user=user, file_path="dummy.xlsx")
    result = asyncio.run(agent.process({"prompt": "any prompt"}))
    assert result == {"result": "processed"}
    mock_process_local_file.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.core_services.models.AgentMemory.objects.update_or_create')
def test_qa_agent_process_ask_and_answer(mock_update_or_create):
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "ask What is your name? Answer: My name is Bard."}
    result = asyncio.run(agent.process(task))
    assert result == {"result": "Stored QA: 'What is your name?' -> 'My name is Bard.'"}
    mock_update_or_create.assert_called_once_with(
        agent_name="qa",
        key="What is your name?",
        defaults={"value": "My name is Bard."}
    )

@pytest.mark.django_db
@patch('ai_agent.core_services.models.AgentMemory.objects.filter')
def test_qa_agent_process_delete(mock_filter):
    mock_delete = MagicMock()
    mock_delete.delete.return_value = (1, {})
    mock_filter.return_value = mock_delete
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "delete What is your name?"}
    result = asyncio.run(agent.process(task))
    assert result == {"result": "Deleted QA for 'What is your name?'"}
    mock_filter.assert_called_once_with(agent_name="qa", key="What is your name?")

@pytest.mark.django_db
@patch('ai_agent.core_services.models.AgentMemory.objects.filter')
def test_qa_agent_process_get_answer(mock_filter):
    mock_mem = MagicMock()
    mock_mem.value = "My name is Bard."
    mock_filter.return_value.first.return_value = mock_mem
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "What is your name?"}
    result = asyncio.run(agent.process(task))
    assert result == {"result": "Answer: My name is Bard."}
    mock_filter.assert_called_once_with(agent_name="qa", key="What is your name?")

@pytest.mark.django_db
@patch('ai_agent.core_services.agents.qa.openai.chat.completions.create')
@patch('ai_agent.core_services.models.AgentMemory.objects.filter')
def test_qa_agent_process_openai_answer(mock_filter, mock_create):
    mock_filter.return_value.first.return_value = None
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'My name is Bard.'})]
    mock_create.return_value = mock_response
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "What is your name?"}
    result = asyncio.run(agent.process(task))
    assert result == {"result": "Answer: My name is Bard."}
    mock_create.assert_called_once()
    # Also check that the answer was stored
    # This part is tricky because of async and mocks. A better way would be to check the db.
    # For now, we assume the logic inside the method is correct if called.
    # A separate integration test would be better.
    
@pytest.mark.django_db
@patch('ai_agent.core_services.agents.qa.QAPairAgent.search_knowledge_base')
@patch('ai_agent.core_services.agents.qa.openai.chat.completions.create')
@patch('ai_agent.core_services.models.AgentMemory.objects.filter')
def test_qa_agent_rag_workflow(mock_filter, mock_create, mock_search):
    # No answer in memory
    mock_filter.return_value.first.return_value = None
    
    # Context found in knowledge base
    mock_search.return_value = ["Kiarash is a developer."]
    
    # OpenAI will answer based on context
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'Kiarash is a developer.'})]
    mock_create.return_value = mock_response
    
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "Who is Kiarash?"}
    
    result = asyncio.run(agent.process(task))
    
    # Verify that search was called
    mock_search.assert_called_once_with("Who is Kiarash?")
    
    # Verify that OpenAI was called with the augmented prompt
    mock_create.assert_called_once()
    args, kwargs = mock_create.call_args
    system_prompt = kwargs['messages'][0]['content']
    assert "Context:" in system_prompt
    assert "Kiarash is a developer." in system_prompt
    
    # Verify the final answer
    assert result['result'] == "Answer: Kiarash is a developer."
    
@pytest.mark.django_db
@freeze_time("2025-10-04 18:20:08")
def test_agent_log_string_representation():
    log = AgentLog.objects.create(agent_name="TestAgent", prompt="Test Prompt")
    assert str(log) == "TestAgent @ 2025-10-04 18:20:08+00:00"


@pytest.mark.django_db
def test_agent_memory_string_representation():
    memory = AgentMemory(agent_name="TestAgent", key="TestKey")
    assert str(memory) == "TestAgent:TestKey"


@pytest.mark.django_db
@patch('ai_agent.agent.agent_manager.QAPairAgent.process')
def test_agent_router_route_to_qa(mock_process):
    mock_process.return_value = {"result": "QA agent processed"}
    router = AgentRouter()
    result = asyncio.run(router.route("ask something"))
    assert result == "QA agent processed"
    mock_process.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.agent.agent_manager.EmailAgent.process')
def test_agent_router_route_to_email(mock_process):
    mock_process.return_value = {"result": "Email agent processed"}
    router = AgentRouter()
    result = asyncio.run(router.route("send an email"))
    assert result == "Email agent processed"
    mock_process.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.agent.agent_manager.QAPairAgent.process')
def test_agent_router_route_default_to_qa(mock_process):
    mock_process.return_value = {"result": "QA agent processed"}
    router = AgentRouter()
    result = asyncio.run(router.route("some unknown prompt"))
    assert result == "QA agent processed"
    mock_process.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.core_services.agents.base.es_client')
@patch('ai_agent.core_services.agents.qa.openai.chat.completions.create')
@patch('ai_agent.core_services.models.AgentMemory.objects.filter')
def test_qa_agent_rag_integration(mock_filter, mock_create, mock_es_client):
    # No answer in memory
    mock_filter.return_value.first.return_value = None
    
    # Context found in knowledge base
    mock_es_client.search.return_value = {
        "hits": {
            "hits": [
                {"_source": {"content": "Kiarash is a developer."}}
            ]
        }
    }
    
    # OpenAI will answer based on context
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={'content': 'Kiarash is a developer.'})]
    mock_create.return_value = mock_response
    
    agent = QAPairAgent(agent_id="qa", name="qa")
    task = {"prompt": "Who is Kiarash?"}
    
    result = asyncio.run(agent.process(task))
    
    # Verify that search was called
    mock_es_client.search.assert_called_once_with(
        index="knowledge_base",
        body={
            "query": {
                "match": {
                    "content": "Who is Kiarash?"
                }
            }
        }
    )
    
    # Verify that OpenAI was called with the augmented prompt
    mock_create.assert_called_once()
    args, kwargs = mock_create.call_args
    system_prompt = kwargs['messages'][0]['content']
    assert "Context:" in system_prompt
    assert "Kiarash is a developer." in system_prompt
    
    # Verify the final answer
    assert result['result'] == "Answer: Kiarash is a developer."