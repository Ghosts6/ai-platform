from django.core.management.base import BaseCommand
from ai_agent.agent.agent_manager import AgentRouter
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Manually trigger an agent task from the CLI.'

    def add_arguments(self, parser):
        parser.add_argument('prompt', type=str, help='Prompt to send to the agent system')
        parser.add_argument('--user', type=str, help='The username of the user to run the agent as')
        parser.add_argument('--agent', type=str, help='The name of the agent to use')

    def handle(self, *args, **options):
        prompt = options['prompt']
        username = options['user']
        agent_key = options['agent']
        
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.SUCCESS(f"Running as user: {user.username}"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User '{username}' not found."))
                return

        router = AgentRouter()
        
        async def run_agent():
            response = await router.route(prompt=prompt, user=user, agent_key=agent_key)
            self.stdout.write(self.style.SUCCESS(f'Agent response: {response}'))

        async_to_sync(run_agent)()
