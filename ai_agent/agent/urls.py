from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('respond/', views.respond_to_prompt, name='respond_to_prompt'),
]
