from django.apps import AppConfig
from pathlib import Path


class SchedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.scheduler"
    path = str(Path(__file__).resolve().parent)
