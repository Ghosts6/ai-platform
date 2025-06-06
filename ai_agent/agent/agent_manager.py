from core_services.agents.echo import EchoAgent
from core_services.agents.summarize import SummarizerAgent
# Import new agents
from core_services.agents.email import EmailAgent
from core_services.agents.excel import ExcelAgent
from core_services.models import AgentLog

class AgentRouter:
    def __init__(self):
        self.agents = {}
        self.routing_rules = []
        self.register_agent("echo", EchoAgent("echo"), keywords=["echo"])
        self.register_agent("summarize", SummarizerAgent("summarize"), keywords=["summarize", "summary"])
        self.register_agent("email", EmailAgent("email"), keywords=["email", "inbox", "mail"]) 
        self.register_agent("excel", ExcelAgent("excel"), keywords=["excel", "spreadsheet", "sheet"])

    def register_agent(self, name, agent, keywords=None):
        self.agents[name] = agent
        if keywords:
            self.routing_rules.append((keywords, agent))

    def route(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        for keywords, agent in self.routing_rules:
            if any(word in prompt_lower for word in keywords):
                response = agent.handle(prompt)
                AgentLog.objects.create(agent_name=agent.name, prompt=prompt, response=response)
                return response
        response = self.agents["echo"].handle(prompt)
        AgentLog.objects.create(agent_name="echo", prompt=prompt, response=response)
        return response
