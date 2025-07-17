from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.apps import apps

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Honeypot

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'website']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        website = validated_data.pop('website', '')
        if website:
            raise serializers.ValidationError({'website': 'Bot detected.'})
        validated_data.pop('profile', None)  # Remove profile if present, signal will handle creation
        user = User.objects.create_user(**validated_data)
        return user
