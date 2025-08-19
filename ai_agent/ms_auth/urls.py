from django.urls import path
from . import views

app_name = 'ms_auth'

urlpatterns = [
    path('login/', views.microsoft_login, name='login'),
    path('callback/', views.microsoft_callback, name='callback'),
    path('error/', views.error, name='error'),
]