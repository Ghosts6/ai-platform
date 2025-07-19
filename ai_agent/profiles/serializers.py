from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile
from django.apps import apps
import re

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Honeypot
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'profile', 'website']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'min_length': 3, 'max_length': 150},
            'email': {'required': True}
        }

    def validate_password(self, value):
        """
        Validate password strength and ensure it meets security requirements
        """
        # Check for common patterns
        if value.lower() in ['password', '123456', 'qwerty', 'admin']:
            raise serializers.ValidationError("Password is too common. Please choose a stronger password.")
        
        # Check for username in password
        initial_data = getattr(self, 'initial_data', {}) or {}
        username = initial_data.get('username', '').lower()
        if username and username in value.lower():
            raise serializers.ValidationError("Password cannot contain your username.")
        
        # Check for email in password
        email = initial_data.get('email', '').lower()
        if email and email.split('@')[0] in value.lower():
            raise serializers.ValidationError("Password cannot contain your email username.")
        
        # Use Django's built-in password validation
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages[0])
        
        return value

    def validate(self, attrs):
        """
        Validate that passwords match and perform additional checks
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Check for common email patterns
        email = attrs.get('email', '')
        if email:
            # Simple email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise serializers.ValidationError("Please enter a valid email address.")
        
        return attrs

    def create(self, validated_data):
        website = validated_data.pop('website', '')
        confirm_password = validated_data.pop('confirm_password', None)
        
        if website:
            raise serializers.ValidationError({'website': 'Bot detected.'})
        
        validated_data.pop('profile', None)  # Remove profile if present, signal will handle creation
        
        # Create user with Django's built-in password hashing
        user = User.objects.create_user(**validated_data)
        
        # Log user creation for security monitoring
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"New user registered: {user.username} ({user.email})")
        
        return user

    def update(self, instance, validated_data):
        """
        Handle password updates securely
        """
        website = validated_data.pop('website', '')
        confirm_password = validated_data.pop('confirm_password', None)
        
        if website:
            raise serializers.ValidationError({'website': 'Bot detected.'})
        
        # Handle password update
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)  # This will hash the password properly
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
