from core_services.agents.summarize import SummarizerAgent
from core_services.agents.qa import QAPairAgent
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.models import AgentLog, AgentMemory
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class AgentRouter:
    def __init__(self):
        self.agents = {
            "summarize": SummarizerAgent("summarize", memory_backend=self.memory_backend),
            "qa": QAPairAgent("qa"),
            "email": EmailAgent("email"),
            "excel": ExcelAgent("excel"),
        }
        self.routing_rules = []
        self.register_agent("summarize", self.agents["summarize"], keywords=["summarize", "summary"])
        self.register_agent("qa", self.agents["qa"], keywords=["ask", "answer:", "list qas", "delete ", "update "])
        self.register_agent("email", self.agents["email"], keywords=["email", "inbox", "mail", "draft", "analyze", "reply", "send", "compose", "attachment"])
        self.register_agent("excel", self.agents["excel"], keywords=["excel", "spreadsheet", "sheet", "analyze", "table", "csv", "cell", "formula"])

    def register_agent(self, name, agent, keywords=None):
        self.agents[name] = agent
        if keywords:
            self.routing_rules.append((keywords, agent))

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
        # AI-powered agent selection: choose the agent with the most relevant keywords in the prompt
        best_agent = None
        best_score = 0
        for keywords, agent in self.routing_rules:
            score = sum(1 for word in keywords if word in prompt_lower)
            if score > best_score:
                best_score = score
                best_agent = agent
        if best_agent:
            return best_agent.handle(prompt)
        # Fallback: use QA agent for all other questions (AI-powered)
        return self.agents["qa"].handle(prompt)
