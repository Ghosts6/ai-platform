from core_services.agents.summarize import SummarizerAgent
from core_services.agents.qa import QAPairAgent
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.agents.teams import TeamsAgent
from core_services.models import AgentLog, AgentMemory
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class AgentRouter:
    def __init__(self):
        self.agent_classes = {
            "summarize": lambda: SummarizerAgent("summarize", memory_backend=self.memory_backend),
            "qa": lambda: QAPairAgent("qa"),
            "email": lambda: EmailAgent("email"),
            "excel": lambda: ExcelAgent("excel"),
            "teams": lambda: TeamsAgent("teams"),
        }
        self.routing_rules = []
        self.register_agent("summarize", "summarize", keywords=["summarize", "summary"])
        self.register_agent("qa", "qa", keywords=["ask", "answer:", "list qas", "delete ", "update "])
        self.register_agent("email", "email", keywords=["email", "inbox", "mail", "draft", "analyze", "reply", "send", "compose", "attachment"])
        self.register_agent("excel", "excel", keywords=["excel", "spreadsheet", "sheet", "analyze", "table", "csv", "cell", "formula"])
        self.register_agent("teams", "teams", keywords=["teams", "maintenance", "survey", "test running", "calendar", "meeting"])

    def register_agent(self, name, agent_key, keywords=None):
        if keywords:
            self.routing_rules.append((keywords, agent_key))

    def memory_backend(self, agent_name, key, value=None):
        if value is not None:
            obj, _ = AgentMemory.objects.update_or_create(
                agent_name=agent_name, key=key, defaults={"value": value}
            )
            return obj.value
        try:
            return AgentMemory.objects.get(agent_name=agent_name, key=key).value
        except AgentMemory.DoesNotExist:
            return None

    def route(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        best_agent_key = None
        best_score = 0
        for keywords, agent_key in self.routing_rules:
            score = sum(1 for word in keywords if word in prompt_lower)
            if score > best_score:
                best_score = score
                best_agent_key = agent_key
        if best_agent_key:
            agent = self.agent_classes[best_agent_key]()
            return agent.handle(prompt)
        # Fallback: use QA agent for all other questions (AI-powered)
        return self.agent_classes["qa"]().handle(prompt)
