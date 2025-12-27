from django.core.management.base import BaseCommand
from ai_agent.core_services.models import Agent, User
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with default agents.'

    def handle(self, *args, **options):
        # Create a superuser if one doesn't exist to assign agents to
        # In a real scenario, agents might be assigned to a specific system user
        # or be globally available. For seeding, we'll create/use a superuser.
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser(
                username='admin', 
                email='admin@example.com', 
                password='adminpassword' # Consider using a more secure way in production
            )
            self.stdout.write(self.style.SUCCESS('Created default superuser: admin'))
        
        default_agents = [
            {'name': 'qa', 'agent_type': 'qa', 'description': 'A general purpose Q&A agent.'},
            {'name': 'email', 'agent_type': 'email', 'description': 'Agent for managing emails.'},
            {'name': 'excel', 'agent_type': 'excel', 'description': 'Agent for Excel operations.'},
            {'name': 'calendar', 'agent_type': 'calendar', 'description': 'Agent for calendar management.'},
            {'name': 'teams', 'agent_type': 'teams', 'description': 'Agent for Microsoft Teams interactions.'},
            {'name': 'summarize', 'agent_type': 'summarize', 'description': 'Agent for summarizing text.'},
            {'name': 'list', 'agent_type': 'list', 'description': 'Agent for managing lists.'},
        ]

        with transaction.atomic():
            for agent_data in default_agents:
                agent, created = Agent.objects.get_or_create(
                    name=agent_data['name'],
                    defaults={
                        'agent_type': agent_data['agent_type'],
                        'description': agent_data['description'],
                        'created_by': admin_user # Assign to the admin user
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Seeded agent: {agent.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Agent '{agent.name}' already exists. Skipping."))