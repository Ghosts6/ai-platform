from ai_agent.core_services.models import Agent
from ai_agent.core_services.agents.base import AgentBase
from asgiref.sync import sync_to_async
import openai
import os
import asyncio
import importlib
import inspect
import pkgutil
import logging

logger = logging.getLogger(__name__)

class AgentRouter:
    def __init__(self):
        self.agent_classes = {}
        self.client = openai.OpenAI()
        self._load_agent_classes()

        self.routing_rules = []
        # These keywords should ideally be stored in the Agent model in the database
        self.register_agent("summarize", "summarize", keywords=["summarize", "summary"])
        self.register_agent("qa", "qa", keywords=["ask", "answer:", "list qas", "delete ", "update "])
        self.register_agent("email", "email", keywords=["email", "inbox", "mail", "draft", "analyze", "reply", "send", "compose", "attachment"])
        self.register_agent("excel", "excel", keywords=["excel", "spreadsheet", "sheet", "analyze", "table", "csv", "cell", "formula"])
        self.register_agent("teams", "teams", keywords=["teams", "maintenance", "survey", "test running"])
        self.register_agent("calendar", "calendar", keywords=["calendar", "event", "meeting", "appointment"])

    def _load_agent_classes(self):
        """Dynamically loads agent classes from the agents directory."""
        agents_package = "ai_agent.core_services.agents"
        package_path = os.path.join(os.path.dirname(__file__), '..', 'core_services', 'agents')

        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            if module_name not in ["base", "list"]: # Exclude base and deprecated list agent
                try:
                    module = importlib.import_module(f".{module_name}", package=agents_package)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, AgentBase) and obj is not AgentBase:
                            # Use the module name as the agent_type key
                            agent_type = module_name.lower()
                            self.agent_classes[agent_type] = obj
                            logger.info(f"Dynamically loaded agent: {agent_type} -> {name}")
                except Exception as e:
                    logger.error(f"Failed to load agent from module {module_name}: {e}")

    def register_agent(self, name, agent_key, keywords=None):
        if keywords:
            self.routing_rules.append((keywords, agent_key))

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
            best_agent_key = "qa"  # Default agent

        agent_class = self.agent_classes.get(best_agent_key)
        if not agent_class:
            return f"Error: Agent '{best_agent_key}' not found."

        try:
            # Fetch the Agent model instance from the database
            agent_model = await sync_to_async(Agent.objects.get)(name=best_agent_key)
        except Agent.DoesNotExist:
            return f"Error: Agent model '{best_agent_key}' not found in database."
        
        # Instantiate the agent with the model instance and other dependencies
        agent = agent_class(
            agent_instance=agent_model, 
            client=self.client, 
            user=user, 
            file_path=file_path
        )

        task = {"prompt": prompt, "type": "text"} # Ensure task has a type
        result = await agent.handle_task(task) # Use handle_task for logging and state management
        
        return result.get("result", result.get("error", "No result returned."))