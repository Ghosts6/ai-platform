from django.apps import AppConfig
from pathlib import Path


class AgentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.agent"
    path = str(Path(__file__).resolve().parent)
