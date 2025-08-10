from rest_framework import serializers
from .models import Agent, Task, AgentConfiguration, Workflow, WorkflowStep, ChatSession, ChatMessage, AgentLog, AgentMemory, ContactMessage

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'messages']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender', 'text', 'created_at']

class AgentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentLog
        fields = ['id', 'agent_name', 'prompt', 'response', 'created_at']

class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = ['id', 'agent_name', 'key', 'value', 'updated_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']

# Enhanced serializers for new models
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            'id', 'name', 'agent_type', 'description', 'version',
            'is_active', 'status', 'configuration', 'capabilities',
            'created_by', 'created_at', 'updated_at', 'last_used'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'user', 'agent', 'task_type', 'input_data',
            'output_data', 'status', 'priority', 'error_message',
            'started_at', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AgentConfigurationSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    
    class Meta:
        model = AgentConfiguration
        fields = [
            'id', 'agent', 'agent_name', 'name', 'configuration',
            'is_active', 'created_at', 'updated_at'
        ]

class WorkflowStepSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    
    class Meta:
        model = WorkflowStep
        fields = ['id', 'agent', 'agent_name', 'step_order', 'configuration']

class WorkflowSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(source='workflowstep_set', many=True, read_only=True)
    
    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'agents', 'configuration',
            'is_active', 'created_at', 'updated_at', 'steps'
        ]