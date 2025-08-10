import pytest
from django.contrib.auth.models import User
from core_services.models import Agent, Task, AgentConfiguration, Workflow, WorkflowStep
from core_services.serializers import AgentSerializer, TaskSerializer, AgentConfigurationSerializer, WorkflowSerializer, WorkflowStepSerializer

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.mark.django_db
def test_agent_serializer(user):
    agent = Agent.objects.create(name="Test Agent", agent_type="custom", created_by=user)
    serializer = AgentSerializer(agent)
    data = serializer.data
    assert data['name'] == "Test Agent"
    assert data['agent_type'] == "custom"
    assert data['created_by'] == user.id

@pytest.mark.django_db
def test_task_serializer(user):
    agent = Agent.objects.create(name="Test Agent", agent_type="custom", created_by=user)
    task = Task.objects.create(user=user, agent=agent, task_type="test_task", input_data={"foo": "bar"})
    serializer = TaskSerializer(task)
    data = serializer.data
    assert data['user'] == user.id
    assert data['agent'] == agent.id
    assert data['task_type'] == "test_task"
    assert data['input_data'] == {"foo": "bar"}

@pytest.mark.django_db
def test_agent_configuration_serializer(user):
    agent = Agent.objects.create(name="Test Agent", agent_type="custom", created_by=user)
    config = AgentConfiguration.objects.create(agent=agent, user=user, name="Test Config", configuration={"key": "value"})
    serializer = AgentConfigurationSerializer(config)
    data = serializer.data
    assert data['agent'] == agent.id
    assert data['name'] == "Test Config"
    assert data['configuration'] == {"key": "value"}

@pytest.mark.django_db
def test_workflow_serializer(user):
    workflow = Workflow.objects.create(name="Test Workflow", user=user)
    agent1 = Agent.objects.create(name="Agent 1", agent_type="custom", created_by=user)
    agent2 = Agent.objects.create(name="Agent 2", agent_type="custom", created_by=user)
    WorkflowStep.objects.create(workflow=workflow, agent=agent1, step_order=1)
    WorkflowStep.objects.create(workflow=workflow, agent=agent2, step_order=2)
    serializer = WorkflowSerializer(workflow)
    data = serializer.data
    assert data['name'] == "Test Workflow"
    assert len(data['steps']) == 2