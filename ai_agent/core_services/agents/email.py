from .base import AgentBase
from typing import Dict, Any, List, Optional
import os
from O365 import Account
from profiles.models import O365Token
import datetime

class EmailAgent(AgentBase):
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
                    self.account = Account(credentials, auth_flow_type='authorization', token=token)
            except O365Token.DoesNotExist:
                pass

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        if not self.account or not self.account.is_authenticated:
            return {"result": "EmailAgent: Please authenticate with Microsoft to use email features. You can do so by visiting /ms_auth/login"}

        # Example: Get number of unread emails
        if "unread" in prompt.lower():
            mailbox = self.account.mailbox()
            inbox = mailbox.inbox_folder()
            return {"result": f"EmailAgent: You have {inbox.unread_count} unread emails."}

        return {"result": "EmailAgent: I am connected to your email account. What would you like to do?"}


    def get_capabilities(self) -> List[str]:
        return ["read_unread_emails", "send_email"]

