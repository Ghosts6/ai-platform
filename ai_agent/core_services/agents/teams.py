from .base import AgentBase
import os
from O365 import Account, FileSystemTokenBackend

class TeamsAgent(AgentBase):
    def __init__(self, name: str):
        super().__init__(name)
        credentials = (
            os.getenv("MS_CLIENT_ID"),
            os.getenv("MS_CLIENT_SECRET")
        )
        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
        self.account = Account(credentials, token_backend=token_backend, tenant_id=os.getenv("MS_TENANT_ID"))
        if not self.account.is_authenticated:
            # You must authenticate interactively once to get the token
            # After that, the token will be reused from o365_token.txt
            self.account.authenticate(scopes=[
                'basic',
                'message_all',
                'calendar_all',
                'offline_access',
            ])

    def handle(self, prompt: str) -> str:
        # Example: create a calendar event if prompt contains certain keywords
        keywords = ["maintenance", "survey", "test running"]
        if any(word in prompt.lower() for word in keywords):
            schedule = self.account.schedule()
            calendar = schedule.get_default_calendar()
            event = calendar.new_event()
            event.subject = f"Automated: {prompt[:50]}"
            event.start = None  # You should parse a date/time from the prompt
            event.end = None    # You should parse a date/time from the prompt
            event.location = "Microsoft Teams"
            event.body = prompt
            # For demo, just save as draft (not send)
            event.save()
            return f"TeamsAgent: Created calendar event for '{prompt[:50]}...'"
        return "TeamsAgent: No relevant action triggered."
