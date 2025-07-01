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
    path('api/agent/', include('agent.urls')),
    path('core/', include('core_services.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('utils/', include('shared_utils.urls')),
    path('', views.index, name='home_index'),

        # media config
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # static files config
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # catch all react patterns - must be last
    re_path(r'^.*$', home_views.index, name='home'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# Serve the frontend app in production
if not settings.DEBUG:
    urlpatterns += [
        path('', TemplateView.as_view(template_name='index.html')),
        path('<path:path>', TemplateView.as_view(template_name='index.html')),
    ]