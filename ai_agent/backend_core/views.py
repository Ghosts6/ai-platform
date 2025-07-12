from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from django.http import FileResponse, Http404
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

def custom_404(request):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

class ReadmeView(View):
    def get(self, request):
        readme_path = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'README.md'))
        if os.path.exists(readme_path):
            return FileResponse(open(readme_path, 'rb'), content_type='text/markdown')
        raise Http404("README.md not found")