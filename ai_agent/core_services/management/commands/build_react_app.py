import os
import subprocess
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Builds React app and runs collectstatic.'

    def handle(self, *args, **kwargs):
        # Project root: ai_agent/..
        project_root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..'))
        frontend_dir = os.path.join(project_root_dir, 'frontend')
        if not os.path.isdir(frontend_dir):
            self.stdout.write(self.style.ERROR(f"Frontend directory not found at {frontend_dir}"))
            return

        self.stdout.write(self.style.WARNING('Building React app...'))
        try:
            subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
            self.stdout.write(self.style.SUCCESS('React app built successfully.'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while building React app: {e}"))
            return

        self.stdout.write(self.style.WARNING('Running collectstatic...'))
        try:
            call_command('collectstatic', '--noinput')
            self.stdout.write(self.style.SUCCESS('collectstatic completed successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred during collectstatic: {e}"))
            return