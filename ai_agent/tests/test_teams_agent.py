import pytest
from unittest.mock import patch, MagicMock
from core_services.agents.teams import TeamsAgent

@pytest.mark.django_db
def test_teams_agent_creates_event(monkeypatch):
    # Mock O365 Account and Calendar
    class DummyEvent:
        def __init__(self):
            self.subject = None
            self.start = None
            self.end = None
            self.location = None
            self.body = None
            self.saved = False
        def save(self):
            self.saved = True
    class DummyCalendar:
        def new_event(self):
            return DummyEvent()
    class DummySchedule:
        def get_default_calendar(self):
            return DummyCalendar()
    class DummyAccount:
        is_authenticated = True
        def schedule(self):
            return DummySchedule()
    monkeypatch.setattr("core_services.agents.teams.Account", lambda *a, **kw: DummyAccount())
    agent = TeamsAgent("teams")
    result = agent.handle("maintenance window on Friday")
    assert "Created calendar event" in result

@pytest.mark.django_db
def test_teams_agent_no_action(monkeypatch):
    class DummyAccount:
        is_authenticated = True
        def schedule(self):
            class DummySchedule:
                def get_default_calendar(self):
                    class DummyCalendar:
                        def new_event(self):
                            class DummyEvent:
                                def save(self): pass
                            return DummyEvent()
                    return DummyCalendar()
            return DummySchedule()
    monkeypatch.setattr("core_services.agents.teams.Account", lambda *a, **kw: DummyAccount())
    agent = TeamsAgent("teams")
    result = agent.handle("random unrelated prompt")
    assert "No relevant action" in result
