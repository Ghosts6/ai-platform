import os
import subprocess
from django.core.management.base import BaseCommand
from django.core.management import call_command
import shutil

class Command(BaseCommand):
    help = 'Builds React app, cleans old static files, and runs collectstatic.'

    def handle(self, *args, **kwargs):
        # Project root: ai_agent/..
        project_root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..'))
        frontend_dir = os.path.join(project_root_dir, 'frontend')
        staticfiles_dir = os.path.join(project_root_dir, 'ai_agent', 'staticfiles')
        dist_dir = os.path.join(frontend_dir, 'dist')

        # Clean old static files
        self.stdout.write(self.style.WARNING('Cleaning old static files...'))
        try:
            if os.path.exists(staticfiles_dir):
                shutil.rmtree(staticfiles_dir)
                self.stdout.write(self.style.SUCCESS('Old staticfiles directory removed.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while cleaning staticfiles: {e}"))
            return
        try:
            if os.path.exists(dist_dir):
                shutil.rmtree(dist_dir)
                self.stdout.write(self.style.SUCCESS('Old React dist directory removed.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while cleaning dist: {e}"))
            return

        # Build React app
        self.stdout.write(self.style.WARNING('Installing frontend dependencies...'))
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            self.stdout.write(self.style.SUCCESS('Frontend dependencies installed successfully.'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while installing frontend dependencies: {e}"))
            return

        self.stdout.write(self.style.WARNING('Building React app...'))
        try:
            subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
            self.stdout.write(self.style.SUCCESS('React app built successfully.'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while building React app: {e}"))
            return

        # Run collectstatic
        self.stdout.write(self.style.WARNING('Running collectstatic...'))
        try:
            call_command('collectstatic', '--noinput')
            self.stdout.write(self.style.SUCCESS('collectstatic completed successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred during collectstatic: {e}"))
            return