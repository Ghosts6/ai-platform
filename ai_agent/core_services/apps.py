from django.apps import AppConfig
from pathlib import Path


class CoreServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.core_services"
    path = str(Path(__file__).resolve().parent)
