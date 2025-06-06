from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/agent/', include('agent.urls')),
    path('core/', include('core_services.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('utils/', include('shared_utils.urls')),
]
