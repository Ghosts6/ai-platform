from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('respond/', views.respond_to_prompt, name='respond_to_prompt'),
    path('memory/', views.agent_memory, name='agent_memory'),
    path('memory/list/', views.agent_memory_list, name='agent_memory_list'),
    path('memory/delete/', views.agent_memory_delete, name='agent_memory_delete'),
]
