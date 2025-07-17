from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, CustomResetPasswordRequestToken, CustomResetPasswordConfirm

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', CustomResetPasswordRequestToken.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', CustomResetPasswordConfirm.as_view(), name='password_reset_confirm'),
]
