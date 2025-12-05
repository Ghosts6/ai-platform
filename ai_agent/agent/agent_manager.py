from core_services.agents.summarize import SummarizerAgent
from core_services.agents.qa import QAPairAgent
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.agents.teams import TeamsAgent
from core_services.agents.calendar import CalendarAgent
from core_services.models import AgentLog, AgentMemory
import openai
import os
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

class AgentRouter:
    def __init__(self):
        self.agent_classes = {
            "summarize": SummarizerAgent,
            "qa": QAPairAgent,
            "email": EmailAgent,
            "excel": ExcelAgent,
            "teams": TeamsAgent,
            "calendar": CalendarAgent,
        }
        self.routing_rules = []
        self.register_agent("summarize", "summarize", keywords=["summarize", "summary"])
        self.register_agent("qa", "qa", keywords=["ask", "answer:", "list qas", "delete ", "update "])
        self.register_agent("email", "email", keywords=["email", "inbox", "mail", "draft", "analyze", "reply", "send", "compose", "attachment"])
        self.register_agent("excel", "excel", keywords=["excel", "spreadsheet", "sheet", "analyze", "table", "csv", "cell", "formula"])
        self.register_agent("teams", "teams", keywords=["teams", "maintenance", "survey", "test running"])
        self.register_agent("calendar", "calendar", keywords=["calendar", "event", "meeting", "appointment"])


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

    async def route(self, prompt: str, user=None, agent_key=None, file_path=None) -> str:
        best_agent_key = agent_key

        if not best_agent_key:
            prompt_lower = prompt.lower()
            best_score = 0
            for keywords, key in self.routing_rules:
                score = sum(1 for word in keywords if word in prompt_lower)
                if score > best_score:
                    best_score = score
                    best_agent_key = key
        
        if not best_agent_key:
            best_agent_key = "qa"
        
        agent_class = self.agent_classes.get(best_agent_key)
        
        agent_params = {"agent_id": best_agent_key, "name": best_agent_key}
        if best_agent_key in ["email", "excel", "teams", "calendar"]:
            agent_params["user"] = user
            if file_path:
                agent_params["file_path"] = file_path
        elif best_agent_key == "summarize":
            agent_params["memory_backend"] = self.memory_backend

        agent = agent_class(**agent_params)

        task = {"prompt": prompt}
        result = await agent.process(task)
        return result.get("result", result.get("error"))