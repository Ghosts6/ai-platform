from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from backend_core import views as home_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/agent/', include('ai_agent.agent.urls')),
    path('api/profiles/', include('ai_agent.profiles.urls')),
    path('api/core/', include('ai_agent.core_services.urls')),
    path('core/', include('ai_agent.core_services.urls')),
    path('scheduler/', include('ai_agent.scheduler.urls')),
    path('utils/', include('ai_agent.shared_utils.urls')),
    path('ms_auth/', include('ai_agent.ms_auth.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', views.index, name='home_index'),

    # Error handling
    path('custom-404/', views.custom_404, name='custom_404'),
    path('custom-500/', views.custom_500, name='custom_500'),

    # media config
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # static files config
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('README.md', views.ReadmeView.as_view(), name='readme_file'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

# Catch-all for React routing
urlpatterns.append(re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name="index.html")))