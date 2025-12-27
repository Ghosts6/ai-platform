from .base import AgentBase
from typing import Dict, Any, List, Optional
import os
from O365 import Account
from ai_agent.profiles.models import O365Token
from ai_agent.core_services.models import Agent
import datetime
from asgiref.sync import sync_to_async

class TeamsAgent(AgentBase):
    def __init__(self, agent_instance: Agent, user=None, **kwargs):
        super().__init__(agent_instance)
        self.user = user
        self.account = None

    async def _get_account(self):
        if self.account and self.account.is_authenticated:
            return self.account
        
        if self.user and self.user.is_authenticated:
            try:
                token_data = await sync_to_async(O365Token.objects.get)(user=self.user)
                if token_data.token_expiry > datetime.datetime.now(datetime.timezone.utc):
                    credentials = (os.getenv("MS_CLIENT_ID"), os.getenv("MS_CLIENT_SECRET"))
                    token = {
                        'access_token': token_data.access_token,
                        'refresh_token': token_data.refresh_token,
                        'expires_at': token_data.token_expiry.timestamp()
                    }
                    self.account = Account(credentials, auth_flow_type='web', token=token)
                    return self.account
            except O365Token.DoesNotExist:
                return None
        return None

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        account = await self._get_account()
        if not account or not account.is_authenticated:
            return {"result": "TeamsAgent: Please authenticate with Microsoft to use Teams features. You can do so by visiting /ms_auth/login"}

        # Example: create a calendar event if prompt contains certain keywords
        keywords = ["maintenance", "survey", "test running"]
        if any(word in prompt.lower() for word in keywords):
            schedule = account.schedule()
            calendar = schedule.get_default_calendar()
            event = calendar.new_event()
            event.subject = f"Automated: {prompt[:50]}"
            event.start = None  # You should parse a date/time from the prompt
            event.end = None    # You should parse a date/time from the prompt
            event.location = "Microsoft Teams"
            event.body = prompt
            # For demo, just save as draft (not send)
            await sync_to_async(event.save)()
            return {"result": f"TeamsAgent: Created calendar event for '{prompt[:50]}...'"}
        
        return {"result": "TeamsAgent: No relevant action triggered."}

    def get_capabilities(self) -> List[str]:
        return ["create_calendar_event"]
