import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from ai_agent.shared_utils import es_client as es_client_module
from ai_agent.core_services.agents.base import AgentBase
from ai_agent.core_services.models import Agent
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

class DummyAgent(AgentBase):
    async def process(self, task, context=None):
        return {"result": "processed"}

    def get_capabilities(self):
        return ["dummy"]

@pytest.fixture
def dummy_agent(test_user):
    agent_model = Agent.objects.create(name="dummy", agent_type="dummy", created_by=test_user)
    return DummyAgent(agent_instance=agent_model)

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_es_client_patching(dummy_agent):
    with patch('ai_agent.shared_utils.es_client.async_es_client', new_callable=MagicMock) as mock_es_client:
        mock_es_client.search = AsyncMock(return_value={"hits": {"hits": [{"_source": {"content": "patched_test"}}]}})
        
        # Now call the search_knowledge_base which uses es_client_module.async_es_client
        result = await dummy_agent.search_knowledge_base("query")
        
        assert result == ["patched_test"]
        mock_es_client.search.assert_called_once()
        assert isinstance(es_client_module.async_es_client, MagicMock) # This assertion confirms the patching worked
