from django.apps import AppConfig
from pathlib import Path


class MsAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.ms_auth"
    path = str(Path(__file__).resolve().parent)
