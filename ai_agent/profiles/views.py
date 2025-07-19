from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from django.apps import apps
from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Send welcome email
        self.send_welcome_email(user)
        logger.info(f"New user registered: {user.username} ({user.email})")

    def send_welcome_email(self, user):
        """Send welcome email to new user"""
        try:
            subject = 'Welcome to AIAgent Platform!'
            
            # Prepare context for template
            context = {
                'username': user.username,
                'login_url': 'http://localhost:3000/login'  # Update with your domain in production
            }
            
            # Render HTML email
            html_message = render_to_string('emails/welcome_email.html', context)
            
            # Plain text fallback
            plain_message = f"""
            Hello {user.username}!

            Welcome to AIAgent Platform! Your account has been successfully created.

            You can now log in to your account and start using our AI-powered services.

            If you have any questions, please don't hesitate to contact our support team.

            Best regards,
            The AIAgent Team
            """
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Welcome email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")

    def send_password_reset_email(self, user, reset_url):
        """Send password reset email to user"""
        try:
            subject = 'Password Reset Request - AIAgent Platform'
            
            # Prepare context for template
            context = {
                'username': user.username,
                'reset_url': reset_url
            }
            
            # Render HTML email
            html_message = render_to_string('emails/password_reset.html', context)
            
            # Plain text fallback
            plain_message = f"""
            Hello {user.username},

            We received a request to reset your password for your AIAgent Platform account.

            To reset your password, visit this link:
            {reset_url}

            This link will expire in 24 hours for your security.

            If you didn't request this password reset, you can safely ignore this email.

            Best regards,
            The AIAgent Team
            """
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        website = request.data.get('website', '')
        if website:
            return Response({'error': 'Bot detected.'}, status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Rate limiting for login attempts
        client_ip = self.get_client_ip(request)
        cache_key = f"login_attempts_{client_ip}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:  # Max 5 attempts per IP
            logger.warning(f"Too many login attempts from IP: {client_ip}")
            return Response({
                "error": "Too many login attempts. Please try again later."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        if not username or not password:
            cache.set(cache_key, attempts + 1, 300)  # 5 minutes timeout
            return Response({
                "error": "Username and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            # Reset attempts on successful login
            cache.delete(cache_key)
            
            Token = apps.get_model('authtoken', 'Token')
            token, created = Token.objects.get_or_create(user=user)
            
            # Log successful login
            logger.info(f"Successful login for user: {username} from IP: {client_ip}")
            
            return Response({
                "token": token.key,
                "is_admin": user.is_staff or user.is_superuser
            })
        else:
            # Increment failed attempts
            cache.set(cache_key, attempts + 1, 300)  # 5 minutes timeout
            
            # Log failed login attempt
            logger.warning(f"Failed login attempt for username: {username} from IP: {client_ip}")
            
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        website = request.data.get('website', '')
        if website:
            return Response({'error': 'Bot detected.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Rate limiting for password reset requests
        client_ip = self.get_client_ip(request)
        cache_key = f"reset_attempts_{client_ip}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 3:  # Max 3 reset requests per IP per hour
            logger.warning(f"Too many password reset attempts from IP: {client_ip}")
            return Response({
                "error": "Too many password reset attempts. Please try again later."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Increment attempts
        cache.set(cache_key, attempts + 1, 3600)  # 1 hour timeout
        
        response = super().post(request, *args, **kwargs)
        
        # If successful, log the reset request
        if response.status_code in [200, 201]:
            email = request.data.get('email', '')
            logger.info(f"Password reset requested for email: {email} from IP: {client_ip}")
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class CustomResetPasswordConfirm(ResetPasswordConfirm):
    def post(self, request, *args, **kwargs):
        website = request.data.get('website', '')
        if website:
            return Response({'error': 'Bot detected.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().post(request, *args, **kwargs)
        
        # If successful, log the password reset
        if response.status_code in [200, 201]:
            token = request.data.get('token', '')
            logger.info(f"Password reset completed for token: {token[:10]}...")
        
        return response
