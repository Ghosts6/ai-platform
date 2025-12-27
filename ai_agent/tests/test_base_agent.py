import pytest
from ai_agent.core_services.agents.base import AgentBase
from unittest.mock import patch, MagicMock, AsyncMock
import json
import asyncio
from ai_agent.core_services.models import Agent
from django.contrib.auth.models import User
from django.utils import timezone

class DummyAgent(AgentBase):
    async def process(self, task, context=None):
        if task.get("prompt") == "error":
            raise ValueError("Test error")
        await self.store_memory("processed", True)
        return {"result": "processed"}

    def get_capabilities(self):
        return ["dummy"]

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def dummy_agent(test_user):
    agent_model = Agent.objects.create(name="dummy", agent_type="dummy", created_by=test_user)
    return DummyAgent(agent_instance=agent_model)

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_configure(dummy_agent):
    dummy_agent.configure({"key": "value"})
    assert dummy_agent.config == {"key": "value"}

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_status(dummy_agent):
    status = dummy_agent.get_status()
    assert status["agent_id"] == str(dummy_agent.agent_instance.id)
    assert status["name"] == "dummy"
    assert status["status"] == "active"

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_store_and_retrieve_memory(dummy_agent):
    await dummy_agent.store_memory("key", "value")
    retrieved_value = await dummy_agent.retrieve_memory("key")
    assert retrieved_value == "value"

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_validate_task(dummy_agent):
    assert dummy_agent.validate_task({"type": "test", "prompt": "test"})
    assert not dummy_agent.validate_task({"type": "test"})

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_format_response(dummy_agent):
    response = dummy_agent.format_response("result")
    assert response["agent_id"] == str(dummy_agent.agent_instance.id)
    assert response["result"] == "result"

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_repr(dummy_agent):
    assert repr(dummy_agent) == f"<EnhancedAgent(id={dummy_agent.agent_instance.id}, name='dummy', status='active')>"

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.shared_utils.es_client.async_es_client', new_callable=AsyncMock)
async def test_search_knowledge_base(mock_es_client, dummy_agent):
    mock_es_client.search.return_value = {"hits": {"hits": [{"_source": {"content": "test"}}]}}
    result = await dummy_agent.search_knowledge_base("query")
    assert result == ["test"]
    mock_es_client.search.assert_called_once()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
@patch('ai_agent.shared_utils.es_client.async_es_client', None)
async def test_search_knowledge_base_no_es(dummy_agent):
    with pytest.raises(RuntimeError, match="ES client required for RAG but not available"):
        await dummy_agent.search_knowledge_base("query")

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_handle_task(dummy_agent):
    result = await dummy_agent.handle_task({"type": "test", "prompt": "test"})
    assert result["result"]['result'] == "processed"
    # check memory
    value_in_memory = await dummy_agent.retrieve_memory("processed")
    assert value_in_memory is True

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_handle_task_invalid(dummy_agent):
    result = await dummy_agent.handle_task({"prompt": "test"})
    assert "Invalid task structure" in result["result"]

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_handle_task_error(dummy_agent):
    result = await dummy_agent.handle_task({"type": "test", "prompt": "error"})
    assert "An unexpected error occurred" in result["metadata"]['error']
