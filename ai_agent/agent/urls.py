from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('respond/', views.AgentResponseView.as_view(), name='respond_to_prompt'),
]
