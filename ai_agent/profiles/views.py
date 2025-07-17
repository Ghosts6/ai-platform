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

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        website = request.data.get('website', '')
        if website:
            return Response({'error': 'Bot detected.'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            Token = apps.get_model('authtoken', 'Token')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "is_admin": user.is_staff or user.is_superuser
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

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
        return super().post(request, *args, **kwargs)

class CustomResetPasswordConfirm(ResetPasswordConfirm):
    def post(self, request, *args, **kwargs):
        website = request.data.get('website', '')
        if website:
            return Response({'error': 'Bot detected.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)
