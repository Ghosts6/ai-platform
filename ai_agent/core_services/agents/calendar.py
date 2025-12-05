from .base import AgentBase
from typing import Dict, Any, List, Optional
import os
from O365 import Account
from ai_agent.profiles.models import O365Token
import datetime

class CalendarAgent(AgentBase):
    def __init__(self, agent_id: str, name: str, description: str = "", user=None):
        super().__init__(agent_id, name, description)
        self.user = user
        self.account = None
        if self.user and self.user.is_authenticated:
            try:
                token_data = O365Token.objects.get(user=self.user)
                if token_data.token_expiry > datetime.datetime.now(datetime.timezone.utc):
                    credentials = (os.getenv("MS_CLIENT_ID"), os.getenv("MS_CLIENT_SECRET"))
                    token = {
                        'access_token': token_data.access_token,
                        'refresh_token': token_data.refresh_token,
                        'expires_at': token_data.token_expiry.timestamp()
                    }
                    self.account = Account(credentials, auth_flow_type='web', token=token)
            except O365Token.DoesNotExist:
                pass

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        if not self.account or not self.account.is_authenticated:
            return {"result": "CalendarAgent: Please authenticate with Microsoft to use calendar features. You can do so by visiting /ms_auth/login"}

        # Example: List upcoming events
        if "events" in prompt.lower() or "appointments" in prompt.lower():
            schedule = self.account.schedule()
            calendar = schedule.get_default_calendar()
            events = calendar.get_events(query="is_organizer eq true", order_by="start/dateTime asc")
            event_list = [f"{event.subject} at {event.start.strftime('%Y-%m-%d %H:%M')}" for event in events]
            return {"result": f"CalendarAgent: Here are some of your upcoming events: {event_list}"}

        return {"result": "CalendarAgent: I am connected to your calendar. What would you like to do?"}


    def get_capabilities(self) -> List[str]:
        return ["list_events", "create_event"]

__all__ = ["CalendarAgent"]
