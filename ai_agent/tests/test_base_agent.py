import pytest
from ai_agent.core_services.agents.base import AgentBase
from unittest.mock import patch, MagicMock
import json
import asyncio

class DummyAgent(AgentBase):
    async def process(self, task, context=None):
        return {"result": "processed"}

    def get_capabilities(self):
        return ["dummy"]

@pytest.fixture
def dummy_agent():
    return DummyAgent(agent_id="dummy", name="dummy")

def test_configure(dummy_agent):
    dummy_agent.configure({"key": "value"})
    assert dummy_agent.config == {"key": "value"}

def test_get_status(dummy_agent):
    status = dummy_agent.get_status()
    assert status["agent_id"] == "dummy"
    assert status["name"] == "dummy"
    assert status["status"] == "idle"

def test_store_and_retrieve_memory(dummy_agent):
    dummy_agent.store_memory("key", "value")
    assert dummy_agent.retrieve_memory("key") == "value"

def test_validate_task(dummy_agent):
    assert dummy_agent.validate_task({"type": "test", "prompt": "test"})
    assert not dummy_agent.validate_task({"type": "test"})

def test_format_response(dummy_agent):
    response = dummy_agent.format_response("result")
    assert response["agent_id"] == "dummy"
    assert response["result"] == "result"

def test_to_from_json(dummy_agent):
    json_str = dummy_agent.to_json()
    new_agent = DummyAgent.from_json(json_str)
    assert new_agent.agent_id == dummy_agent.agent_id
    assert new_agent.name == dummy_agent.name

def test_repr(dummy_agent):
    assert repr(dummy_agent) == "<EnhancedAgent(id=dummy, name='dummy', status='idle')>"

@patch('ai_agent.core_services.agents.base.es_client')
def test_search_knowledge_base(mock_es_client, dummy_agent):
    mock_es_client.search.return_value = {"hits": {"hits": [{"_source": {"content": "test"}}]}}
    result = dummy_agent.search_knowledge_base("query")
    assert result == ["test"]
    mock_es_client.search.assert_called_once()

@patch('ai_agent.core_services.agents.base.es_client', None)
def test_search_knowledge_base_no_es(dummy_agent):
    result = dummy_agent.search_knowledge_base("query")
    assert result == []

def test_handle_task(dummy_agent):
    result = asyncio.run(dummy_agent.handle_task({"type": "test", "prompt": "test"}))
    assert result["result"] == {"result": "processed"}

def test_handle_task_invalid(dummy_agent):
    result = asyncio.run(dummy_agent.handle_task({"prompt": "test"}))
    assert "Invalid task structure" in result["result"]
