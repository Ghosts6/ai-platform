from django.shortcuts import render, redirect
from django.conf import settings

class RedirectAndMaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check for testing environment
        if getattr(settings, 'IS_TESTING', False):
            return self.get_response(request)

        # 2. Check for maintenance mode
        if getattr(settings, 'MAINTENANCE_MODE', False):
            if not request.path.startswith('/admin/'):
                return render(request, 'maintenance.html', status=503)
            # Allow admin access during maintenance
            return self.get_response(request)

        # 3. Define paths that Django should handle directly
        django_paths = [
            '/admin/',
            '/api/',
        ]
        
        # Add STATIC_URL and MEDIA_URL from settings for safety
        if settings.STATIC_URL:
            django_paths.append(settings.STATIC_URL)
        if settings.MEDIA_URL:
            django_paths.append(settings.MEDIA_URL)
            
        password_reset_url = getattr(settings, 'DJANGO_REST_PASSWORDRESET', {}).get('PASSWORD_RESET_URL')
        if password_reset_url:
            django_paths.append(password_reset_url)

        # Use a set for faster lookups of exact paths
        django_path_set = set(django_paths)

        # 4. Let Django handle the request if the path starts with an allowed prefix
        if any(request.path.startswith(path) for path in django_path_set):
            return self.get_response(request)

        # 5. For any other path, redirect to the root of the frontend application
        return redirect(settings.FRONTEND_URL)