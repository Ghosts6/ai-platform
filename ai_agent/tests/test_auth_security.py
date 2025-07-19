import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.password_validation import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from typing import Any
import json

class AuthSecurityTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        # Clear cache before each test
        cache.clear()

    def test_password_hashing_algorithm(self):
        """Test that passwords are hashed with strong algorithms"""
        # Create a user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        # Check that password is hashed with a strong algorithm
        hasher = identify_hasher(user.password)
        strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
        
        # Verify the hasher algorithm is in our list of strong algorithms
        self.assertTrue(hasattr(hasher, 'algorithm'))
        algorithm = getattr(hasher, 'algorithm', '')
        self.assertIn(algorithm, strong_algorithms)
        
        # Verify password still works
        self.assertTrue(user.check_password('SecurePass123!'))

    def test_password_validation_weak_password(self):
        """Test that weak passwords are rejected during password validation"""
        from django.contrib.auth.password_validation import validate_password
        
        # This should raise an exception for weak password
        with self.assertRaises(ValidationError):
            validate_password('a')  # Too short and too simple

    def test_password_validation_strong_password(self):
        """Test that strong passwords are accepted"""
        # This should work with a strong password
        user = User.objects.create_user(
            username='testuser_strong',
            email='test_strong@example.com',
            password='SecurePass123!'
        )
        
        # Verify user was created successfully
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser_strong')
        
        # Verify password is properly hashed
        hasher = identify_hasher(user.password)
        strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
        self.assertTrue(hasattr(hasher, 'algorithm'))
        algorithm = getattr(hasher, 'algorithm', '')
        self.assertIn(algorithm, strong_algorithms)

    def test_login_rate_limiting(self):
        """Test that login attempts are rate limited after 5 failed attempts"""
        # Create a user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        # Try to login with wrong password 5 times (should not be rate limited yet)
        for i in range(5):
            response = self.client.post(
                '/api/profiles/login/',
                data=json.dumps({
                    'username': 'testuser',
                    'password': 'wrongpassword',
                    'website': ''
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('Invalid credentials', response.data['error'])
        
        # 6th attempt should be rate limited
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('Too many login attempts', response.data['error'])

    def test_login_rate_limiting_reset_on_success(self):
        """Test that rate limiting is reset after successful login"""
        # Create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        # Try to login with wrong password 3 times
        for i in range(3):
            response = self.client.post(
                '/api/profiles/login/',
                data=json.dumps({
                    'username': 'testuser',
                    'password': 'wrongpassword',
                    'website': ''
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Now login with correct password (should reset rate limiting)
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!',
                'website': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Try wrong password again (should not be rate limited since it was reset)
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bot_detection_registration(self):
        """Test that bot detection works during registration"""
        bot_data = self.user_data.copy()
        bot_data['website'] = 'spammy'
        
        response = self.client.post(
            '/api/profiles/register/',
            data=json.dumps(bot_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Bot detected', response.data['website'])

    def test_bot_detection_login(self):
        """Test that bot detection works during login"""
        # Create a user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!',
                'website': 'spammy'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Bot detected', response.data['error'])

    def test_bot_detection_password_reset(self):
        """Test that bot detection works during password reset"""
        response = self.client.post(
            '/api/profiles/password-reset/',
            data=json.dumps({
                'email': 'test@example.com',
                'website': 'spammy'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Bot detected', response.data['error'])

    def test_registration_with_strong_password(self):
        """Test successful registration with strong password"""
        response = self.client.post(
            '/api/profiles/register/',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify user was created
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        
        # Verify password is properly hashed
        hasher = identify_hasher(user.password)
        strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
        self.assertIn(hasher.algorithm, strong_algorithms)

    def test_registration_password_mismatch(self):
        """Test that password confirmation is required"""
        mismatch_data = self.user_data.copy()
        mismatch_data['confirm_password'] = 'DifferentPass123!'
        
        response = self.client.post(
            '/api/profiles/register/',
            data=json.dumps(mismatch_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match', str(response.data))

    def test_registration_weak_password(self):
        """Test that weak passwords are rejected during registration"""
        weak_password_data = self.user_data.copy()
        weak_password_data['password'] = 'weak'
        weak_password_data['confirm_password'] = 'weak'
        
        response = self.client.post(
            '/api/profiles/register/',
            data=json.dumps(weak_password_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        """Test that missing username/password are handled correctly"""
        # Missing username
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'password': 'SecurePass123!',
                'website': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['error'])
        
        # Missing password
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'website': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username and password are required', response.data['error'])

    def test_successful_login(self):
        """Test successful login with correct credentials"""
        # Create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!',
                'website': ''
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('is_admin', response.data)

    def test_logout(self):
        """Test logout functionality"""
        # Create a user and get token
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        token = Token.objects.create(user=user)
        
        # Authenticate client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Test logout
        response = self.client.post('/api/profiles/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify token is deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)

    def test_password_update_security(self):
        """Test that password updates are handled securely"""
        # Create a user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123!'
        )
        
        # Update password through serializer
        from profiles.serializers import UserSerializer
        serializer = UserSerializer(user, data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'NewSecurePass456!',
            'confirm_password': 'NewSecurePass456!'
        }, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        
        # Verify new password works
        self.assertTrue(updated_user.check_password('NewSecurePass456!'))
        
        # Verify old password doesn't work
        self.assertFalse(updated_user.check_password('OldPass123!'))
        
        # Verify password is properly hashed
        hasher = identify_hasher(updated_user.password)
        strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
        self.assertIn(hasher.algorithm, strong_algorithms)

    def test_ip_detection(self):
        """Test that client IP detection works correctly"""
        # Create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        # Test with X-Forwarded-For header
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json',
            HTTP_X_FORWARDED_FOR='192.168.1.1, 10.0.0.1'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test without X-Forwarded-For header
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cache_cleanup(self):
        """Test that cache is properly managed for rate limiting"""
        # Create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        # Make some failed attempts
        for i in range(3):
            self.client.post(
                '/api/profiles/login/',
                data=json.dumps({
                    'username': 'testuser',
                    'password': 'wrongpassword',
                    'website': ''
                }),
                content_type='application/json'
            )
        
        # Verify cache entry exists
        client_ip = '127.0.0.1'  # Default test IP
        cache_key = f"login_attempts_{client_ip}"
        attempts = cache.get(cache_key)
        self.assertEqual(attempts, 3)
        
        # Successful login should clear cache
        response = self.client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!',
                'website': ''
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify cache is cleared
        attempts = cache.get(cache_key)
        self.assertIsNone(attempts) 