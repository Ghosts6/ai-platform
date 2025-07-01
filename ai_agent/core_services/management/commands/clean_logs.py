import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Change directory to Logs and run the clean.sh bash script'

    def handle(self, *args, **kwargs):
        logs_dir = os.path.join(os.path.dirname(__file__), '../../../Logs')
        script_path = os.path.join(logs_dir, 'clean.sh')

        if os.path.exists(script_path):
            self.stdout.write(f"Changing directory to {logs_dir} and running {script_path}")
            try:
                subprocess.run(['bash', script_path], check=True, cwd=logs_dir)
                self.stdout.write(self.style.SUCCESS('Successfully ran clean.sh'))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f"Error running clean.sh: {e}"))
        else:
            self.stderr.write(self.style.ERROR(f"{script_path} does not exist"))