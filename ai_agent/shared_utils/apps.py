from django.apps import AppConfig
from pathlib import Path


class SharedUtilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.shared_utils"
    path = str(Path(__file__).resolve().parent)
