import pytest
import json
from ai_agent.core_services.models import Agent, AgentLog, AgentMemory
from django.contrib.auth.models import User
from django.utils import timezone
from ai_agent.agent.agent_manager import AgentRouter
from ai_agent.core_services.agents.email import EmailAgent
from ai_agent.core_services.agents.excel import ExcelAgent
from ai_agent.core_services.agents.summarize import SummarizerAgent
from ai_agent.core_services.agents.qa import QAPairAgent
from unittest.mock import patch, MagicMock, AsyncMock
from freezegun import freeze_time
from ai_agent.profiles.models import O365Token
import datetime

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.mark.django_db
def test_agentlog_creation(test_user):
    agent = Agent.objects.create(name="test_agent", agent_type="test", created_by=test_user)
    log = AgentLog.objects.create(
        agent=agent,
        prompt="Test prompt",
        response="Test response",
        created_at=timezone.now()
    )
    assert log.pk is not None
    assert log.agent.name == "test_agent"
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
from asgiref.sync import sync_to_async

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.summarize.openai.OpenAI')
async def test_summarizer_agent_openai(mock_openai, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(
        name="summarize",
        defaults={"agent_type": "summarize", "created_by": test_user},
    )

    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="This is a summary."))]
    )

    agent = SummarizerAgent(agent_instance=agent_model)
    result = await agent.process({"prompt": "summarize this text"})

    assert "Summary:" in result["result"]

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.qa.QAPairAgent.search_knowledge_base', new_callable=AsyncMock)
@patch('ai_agent.core_services.agents.qa.openai.OpenAI')
async def test_qa_agent_openai(mock_openai, mock_search_knowledge_base, test_user):
    mock_search_knowledge_base.return_value = []
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})

    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='Paris'))]
    )

    agent = QAPairAgent(agent_instance=agent_model)
    result = await agent.process({"prompt": "What is the capital of France?"})
    assert "Answer:" in result['result']
    # Should be stored in memory
    mem = await sync_to_async(AgentMemory.objects.get)(agent_name="qa", key="What is the capital of France?")
    assert "Paris" in mem.value

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_agent_router_initialization(test_user):
    await sync_to_async(Agent.objects.get_or_create)(name="summarize", defaults={"agent_type": "summarize", "created_by": test_user})
    await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    await sync_to_async(Agent.objects.get_or_create)(name="email", defaults={"agent_type": "email", "created_by": test_user})
    await sync_to_async(Agent.objects.get_or_create)(name="excel", defaults={"agent_type": "excel", "created_by": test_user})
    await sync_to_async(Agent.objects.get_or_create)(name="teams", defaults={"agent_type": "teams", "created_by": test_user})
    await sync_to_async(Agent.objects.get_or_create)(name="calendar", defaults={"agent_type": "calendar", "created_by": test_user})
    router = AgentRouter()
    assert "summarize" in router.agent_classes
    assert "qa" in router.agent_classes
    assert "email" in router.agent_classes
    assert "excel" in router.agent_classes
    assert "teams" in router.agent_classes
    assert "calendar" in router.agent_classes
    assert len(router.routing_rules) > 0

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.excel.ExcelAgent._process_local_file')
async def test_excel_agent_process_local_file_called(mock_process_local_file, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(
        name="excel",
        defaults={"agent_type": "excel", "created_by": test_user},
    )

    mock_process_local_file.return_value = {"result": "processed"}

    agent = ExcelAgent(
        agent_instance=agent_model,
        user=test_user,
        file_path="dummy.xlsx",
    )

    result = await agent.process({"prompt": "any prompt"})

    assert result == {"result": "processed"}
    mock_process_local_file.assert_called_once()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_qa_agent_process_ask_and_answer(test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    agent = QAPairAgent(agent_instance=agent_model)
    task = {"prompt": "ask What is your name? Answer: My name is Bard."}
    result = await agent.process(task)
    assert result == {"result": "Stored QA: 'What is your name?' -> 'My name is Bard.'"}
    mem = await sync_to_async(AgentMemory.objects.get)(agent_name="qa", key="What is your name?")
    assert 'Bard' in mem.value

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_qa_agent_process_delete(test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    agent = QAPairAgent(agent_instance=agent_model)
    # First, add a value
    await agent.store_memory("question_to_delete", {"answer": "some answer"})
    
    task = {"prompt": "delete question_to_delete"}
    result = await agent.process(task)
    assert result == {"result": "Deleted QA for 'question_to_delete'"}
    mem = await sync_to_async(AgentMemory.objects.get)(agent_name="qa", key="question_to_delete")
    assert json.loads(mem.value)['value'] is None
    
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_qa_agent_process_get_answer(test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    agent = QAPairAgent(agent_instance=agent_model)
    await agent.store_memory("What is your name?", {"answer": "My name is Bard."})
    task = {"prompt": "What is your name?"}
    result = await agent.process(task)
    assert result == {"result": "Answer: My name is Bard."}

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.qa.QAPairAgent.search_knowledge_base', new_callable=AsyncMock)
@patch('ai_agent.core_services.agents.qa.openai.OpenAI')
async def test_qa_agent_process_openai_answer(mock_openai, mock_search_knowledge_base, test_user):
    mock_search_knowledge_base.return_value = []

    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(
                    content="I am an AI language model created by OpenAI."
                )
            )
        ]
    )

    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(
        name="qa",
        defaults={"agent_type": "qa", "created_by": test_user},
    )

    agent = QAPairAgent(agent_instance=agent_model)
    result = await agent.process({"prompt": "What is your name?"})

    assert result == {
        "result": "Answer: I am an AI language model created by OpenAI."
    }

    mock_client.chat.completions.create.assert_called_once()

@pytest.mark.django_db
@freeze_time("2025-10-04 18:20:08")
def test_agent_log_string_representation(test_user):
    agent = Agent.objects.create(name="TestAgent", agent_type="test", created_by=test_user)
    log = AgentLog.objects.create(agent=agent, prompt="Test Prompt")
    assert str(log) == "TestAgent @ 2025-10-04 18:20:08+00:00"


@pytest.mark.django_db
def test_agent_memory_string_representation():
    memory = AgentMemory(agent_name="TestAgent", key="TestKey")
    assert str(memory) == "TestAgent:TestKey"

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.qa.QAPairAgent.process')
async def test_agent_router_route_to_qa(mock_process, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    mock_process.return_value = {"result": "QA agent processed"}
    router = await sync_to_async(AgentRouter)()
    result = await router.route("ask something", user=test_user)
    assert result == {"result": "QA agent processed"}
    mock_process.assert_called_once()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.email.EmailAgent.process')
async def test_agent_router_route_to_email(mock_process, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="email", defaults={"agent_type": "email", "created_by": test_user})
    mock_process.return_value = {"result": "Email agent processed"}
    router = await sync_to_async(AgentRouter)()
    result = await router.route("send an email", user=test_user)
    assert result == {"result": "Email agent processed"}
    mock_process.assert_called_once()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.qa.QAPairAgent.process')
async def test_agent_router_route_default_to_qa(mock_process, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(name="qa", defaults={"agent_type": "qa", "created_by": test_user})
    mock_process.return_value = {"result": "QA agent processed"}
    router = await sync_to_async(AgentRouter)()
    result = await router.route("some unknown prompt", user=test_user)
    assert result == {"result": "QA agent processed"}
    mock_process.assert_called_once()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.core_services.agents.qa.openai.OpenAI')
async def test_qa_agent_rag_integration(mock_openai, test_user):
    agent_model, _ = await sync_to_async(Agent.objects.get_or_create)(
        name="qa",
        defaults={"agent_type": "qa", "created_by": test_user},
    )

    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Kiarash is a developer."))]
    )

    agent = QAPairAgent(agent_instance=agent_model)

    with patch.object(agent, 'search_knowledge_base', new_callable=AsyncMock) as mock_search:
        mock_search.return_value = ["Kiarash is a developer."]

        result = await agent.process({"prompt": "Who is Kiarash?"})

        mock_search.assert_called_once()
        assert result["result"] == "Answer: Kiarash is a developer."