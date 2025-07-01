from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

class ReactAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(settings.STATIC_ROOT, 'frontend', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "index.html not found. Did you run collectstatic and build the React app?",
                status=501,
            )
