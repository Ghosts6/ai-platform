from .base import AgentBase

class EmailAgent(AgentBase):
    def handle(self, prompt: str) -> str:
        # Simple logic: if 'summarize' in prompt, return a fake summary
        if 'summarize' in prompt.lower():
            return "Email Summary: This is a summary of your email."
        elif 'draft' in prompt.lower():
            return "Email Draft: Dear user, ..."
        elif 'reply' in prompt.lower():
            return "Email Reply: Thank you for your message."
        return "EmailAgent: No actionable email task detected."
