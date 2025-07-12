from django.db import models
from django.utils import timezone

# Create your models here.

class AgentLog(models.Model):
    agent_name = models.CharField(max_length=100)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.agent_name} @ {self.created_at}"

class AgentMemory(models.Model):
    agent_name = models.CharField(max_length=100)
    key = models.CharField(max_length=255)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("agent_name", "key")

    def __str__(self):
        return f"{self.agent_name}:{self.key}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"