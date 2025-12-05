from django.apps import AppConfig
from pathlib import Path


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_agent.profiles"
    path = str(Path(__file__).resolve().parent)

    def ready(self):
        import ai_agent.profiles.signals
