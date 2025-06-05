from django.core.management.base import BaseCommand
import pytest

class Command(BaseCommand):
    help = "Runs pytest suite instead of Django's test runner."

    def handle(self, *args, **options):
        exit_code = pytest.main(["tests"])
        raise SystemExit(exit_code)