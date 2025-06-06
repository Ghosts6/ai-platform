from django.core.management.base import BaseCommand
from agent.agent_manager import AgentRouter

class Command(BaseCommand):
    help = 'Manually trigger an agent task from the CLI.'

    def add_arguments(self, parser):
        parser.add_argument('prompt', type=str, help='Prompt to send to the agent system')

    def handle(self, *args, **options):
        prompt = options['prompt']
        router = AgentRouter()
        response = router.route(prompt)
        self.stdout.write(self.style.SUCCESS(f'Agent response: {response}'))
