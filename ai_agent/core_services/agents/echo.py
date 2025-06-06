from .base import AgentBase

class EchoAgent(AgentBase):
    def handle(self, prompt: str) -> str:
        return f"Echo: {prompt}"



