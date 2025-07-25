from django.shortcuts import render
from django.conf import settings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip maintenance mode during tests
        if getattr(settings, 'IS_TESTING', False) or getattr(settings, 'TEST_MODE', False):
            return self.get_response(request)
        if getattr(settings, 'MAINTENANCE_MODE', False) and not request.path.startswith('/admin'):
            return render(request, 'maintenance.html', status=503)
        return self.get_response(request)
