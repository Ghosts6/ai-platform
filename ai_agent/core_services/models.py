from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json
import uuid
class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10) # 'user' or 'agent'
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AgentLog(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('ERROR', 'Error'),
    ]
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SUCCESS')
    duration = models.FloatField(help_text="Duration of the agent's process in seconds", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        agent_name = self.agent.name if self.agent else "N/A"
        return f"{agent_name} @ {self.created_at}"

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

# Enhanced Agent model
class Agent(models.Model):
    """Enhanced Agent model with configuration and metadata"""
    
    AGENT_TYPES = [
        ('email', 'Email Agent'),
        ('excel', 'Excel Agent'),
        ('qa', 'Q&A Agent'),
        ('summarize', 'Summarize Agent'),
        ('teams', 'Teams Agent'),
        ('list', 'List Agent'),
        ('orchestrator', 'Orchestrator Agent'),
        ('custom', 'Custom Agent'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('processing', 'Processing'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, default="1.0.0")
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    configuration = models.JSONField(default=dict, blank=True)
    capabilities = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.agent_type})"

class AgentConfiguration(models.Model):
    """User-specific agent configurations"""
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='configurations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('agent', 'user', 'name')
    
    def __str__(self):
        return f"{self.user.username} - {self.agent.name} - {self.name}"

class Task(models.Model):
    """Tasks to be processed by agents"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    task_type = models.CharField(max_length=50)
    input_data = models.JSONField()
    output_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'created_at']
    
    def __str__(self):
        return f"{self.task_type} - {self.status}"

class Workflow(models.Model):
    """Multi-agent workflows"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agents = models.ManyToManyField(Agent, through='WorkflowStep')
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WorkflowStep(models.Model):
    """Individual steps in a workflow"""
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    step_order = models.PositiveIntegerField()
    configuration = models.JSONField(default=dict)
    depends_on = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    class Meta:
        ordering = ['step_order']
    
    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}: {self.agent.name}"