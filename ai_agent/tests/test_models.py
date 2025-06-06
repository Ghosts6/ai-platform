import pytest
from core_services.models import AgentLog
from django.utils import timezone

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
