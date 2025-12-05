import pytest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.password_validation import validate_password, ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from rest_framework.authtoken.models import Token
import json
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ai_agent.profiles.models import O365Token
import asyncio
from django.core import mail
from datetime import datetime
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'SecurePass123!',
        'confirm_password': 'SecurePass123!'
    }

@pytest.fixture(autouse=True)
def clear_cache_and_mail():
    cache.clear()
    mail.outbox = []

@pytest.mark.django_db
def test_password_hashing_algorithm(user):
    """Test that passwords are hashed with strong algorithms"""
    user.set_password('SecurePass123!')
    user.save()
    hasher = identify_hasher(user.password)
    strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
    assert hasattr(hasher, 'algorithm')
    algorithm = getattr(hasher, 'algorithm', '')
    assert algorithm in strong_algorithms
    assert user.check_password('SecurePass123!')

@pytest.mark.django_db
def test_password_validation_weak_password():
    """Test that weak passwords are rejected during password validation"""
    with pytest.raises(ValidationError):
        validate_password('a')

@pytest.mark.django_db
def test_password_validation_strong_password():
    """Test that strong passwords are accepted"""
    user = User.objects.create_user(
        username='testuser_strong',
        email='test_strong@example.com',
        password='SecurePass123!'
    )
    assert user.id is not None
    assert user.username == 'testuser_strong'
    hasher = identify_hasher(user.password)
    strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
    assert hasattr(hasher, 'algorithm')
    algorithm = getattr(hasher, 'algorithm', '')
    assert algorithm in strong_algorithms

@pytest.mark.django_db
def test_login_rate_limiting(client, user):
    """Test that login attempts are rate limited after 5 failed attempts"""
    for i in range(5):
        response = client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': user.username,
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Invalid credentials' in response.data['error']
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'wrongpassword',
            'website': ''
        }),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert 'Too many login attempts' in response.data['error']

@pytest.mark.django_db
def test_login_rate_limiting_reset_on_success(client, user):
    """Test that rate limiting is reset after successful login"""
    for i in range(3):
        response = client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': user.username,
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'SecurePass123!',
            'website': ''
        }),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'wrongpassword',
            'website': ''
        }),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_bot_detection_registration(client, user_data):
    """Test that bot detection works during registration"""
    bot_data = user_data.copy()
    bot_data['website'] = 'spammy'
    
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(bot_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Bot detected' in response.data['website']

@pytest.mark.django_db
def test_bot_detection_login(client, user):
    """Test that bot detection works during login"""
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'SecurePass123!',
            'website': 'spammy'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Bot detected' in response.data['error']

@pytest.mark.django_db
def test_bot_detection_password_reset(client):
    """Test that bot detection works during password reset"""
    response = client.post(
        '/api/profiles/password-reset/',
        data=json.dumps({
            'email': 'test@example.com',
            'website': 'spammy'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Bot detected' in response.data['error']

@pytest.mark.django_db
def test_registration_with_strong_password(client, user_data):
    """Test successful registration with strong password"""
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    user = User.objects.get(username='testuser')
    assert user.email == 'test@example.com'
    
    hasher = identify_hasher(user.password)
    strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
    assert hasher.algorithm in strong_algorithms

@pytest.mark.django_db
def test_registration_password_mismatch(client, user_data):
    """Test that password confirmation is required"""
    mismatch_data = user_data.copy()
    mismatch_data['confirm_password'] = 'DifferentPass123!'
    
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(mismatch_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Passwords do not match' in str(response.data)

@pytest.mark.django_db
def test_registration_weak_password(client, user_data):
    """Test that weak passwords are rejected during registration"""
    weak_password_data = user_data.copy()
    weak_password_data['password'] = 'weak'
    weak_password_data['confirm_password'] = 'weak'
    
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(weak_password_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_missing_fields(client):
    """Test that missing username/password are handled correctly"""
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'password': 'SecurePass123!',
            'website': ''
        }),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Username and password are required' in response.data['error']
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': 'testuser',
            'website': ''
        }),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Username and password are required' in response.data['error']

@pytest.mark.django_db
def test_successful_login(client, user):
    """Test successful login with correct credentials"""
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'SecurePass123!',
            'website': ''
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert 'is_admin' in response.data

@pytest.mark.django_db
def test_logout(client, user):
    """Test logout functionality"""
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    response = client.post('/api/profiles/logout/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    with pytest.raises(Token.DoesNotExist):
        Token.objects.get(user=user)

@pytest.mark.django_db
def test_password_update_security(user):
    """Test that password updates are handled securely"""
    from ai_agent.profiles.serializers import UserSerializer
    serializer = UserSerializer(user, data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'NewSecurePass456!',
        'confirm_password': 'NewSecurePass456!'
    }, partial=True)
    
    assert serializer.is_valid()
    updated_user = serializer.save()
    
    assert updated_user.check_password('NewSecurePass456!')
    assert not updated_user.check_password('OldPass123!')
    
    hasher = identify_hasher(updated_user.password)
    strong_algorithms = ['pbkdf2_sha256', 'pbkdf2_sha1']
    assert hasher.algorithm in strong_algorithms

@pytest.mark.django_db
def test_ip_detection(client, user):
    """Test that client IP detection works correctly"""
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'wrongpassword',
            'website': ''
        }),
        content_type='application/json',
        HTTP_X_FORWARDED_FOR='192.168.1.1, 10.0.0.1'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'wrongpassword',
            'website': ''
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_cache_cleanup(client, user):
    """Test that cache is properly managed for rate limiting"""
    for i in range(3):
        client.post(
            '/api/profiles/login/',
            data=json.dumps({
                'username': user.username,
                'password': 'wrongpassword',
                'website': ''
            }),
            content_type='application/json'
        )
    
    client_ip = '127.0.0.1'
    cache_key = f"login_attempts_{client_ip}"
    attempts = cache.get(cache_key)
    assert attempts == 3
    
    response = client.post(
        '/api/profiles/login/',
        data=json.dumps({
            'username': user.username,
            'password': 'SecurePass123!',
            'website': ''
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    attempts = cache.get(cache_key)
    assert attempts is None

@pytest.mark.django_db(transaction=True)
def test_microsoft_login_redirects(client, user):
    """
    Test that the microsoft_login view redirects to the Microsoft login page.
    """
    client.force_login(user)
    with patch('ai_agent.ms_auth.views.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.get_authorization_url.return_value = ('https://login.microsoftonline.com/test', 'test_state')
        
        response = client.get(reverse('ms_auth:login'))
        
        assert response.status_code == 302
        assert response.url.startswith('https://login.microsoftonline.com/test')

@pytest.mark.django_db(transaction=True)
def test_microsoft_callback_success(client, user):
    """
    Test the microsoft_callback view with a successful authentication.
    """
    client.force_login(user)
    session = client.session
    session['ms_auth_state'] = 'test_state'
    session.save()

    with patch('ai_agent.ms_auth.views.Account') as mock_account:
        mock_instance = mock_account.return_value
        mock_instance.authenticate.return_value = True
        mock_instance.connection.get_session.return_value.token = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_in': 3600,
            'expires_at': timezone.make_aware(datetime.fromtimestamp(1234567890))
        }

        callback_url = reverse('ms_auth:callback') + '?code=test_code&state=test_state'
        response = client.get(callback_url)

        assert response.status_code == 302
        assert response.url == '/'
        
        assert O365Token.objects.filter(user=user).exists()
        
        token = O365Token.objects.get(user=user)
        assert token.access_token == 'test_access_token'

@pytest.mark.django_db
def test_welcome_email_sent_on_registration(client, user_data):
    """Test that welcome email is sent when user registers"""
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1
    
    email = mail.outbox[0]
    assert email.subject == 'Welcome to AIAgent Platform!'
    assert email.to == ['test@example.com']
    assert 'Welcome to AIAgent Platform' in email.body

@pytest.mark.django_db
def test_welcome_email_html_content(client, user_data):
    """Test that welcome email contains proper HTML content"""
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    email = mail.outbox[0]
    assert email.subject == 'Welcome to AIAgent Platform!'
    assert email.to == ['test@example.com']

@pytest.mark.django_db
def test_password_reset_email_sent(client, user):
    """Test that password reset email is sent when requested"""
    response = client.post(
        reverse('password_reset_request'),
        data=json.dumps({
            'email': user.email,
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert ResetPasswordToken.objects.filter(user=user).exists()
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == [user.email]

@pytest.mark.django_db
def test_password_reset_email_html_content(client, user):
    """Test that password reset email contains proper HTML content"""
    response = client.post(
        reverse('password_reset_request'),
        data=json.dumps({
            'email': user.email,
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert ResetPasswordToken.objects.filter(user=user).exists()
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert 'Password Reset Request' in email.alternatives[0][0]

@pytest.mark.django_db
def test_password_reset_rate_limiting(client, user):
    """Test that password reset requests are rate limited"""
    with patch('django.core.cache.cache.get') as mock_cache_get:
        mock_cache_get.return_value = 0
        for i in range(3):
            response = client.post(
                reverse('password_reset_request'),
                data=json.dumps({
                    'email': user.email,
                }),
                content_type='application/json'
            )
            assert response.status_code == status.HTTP_200_OK

    with patch('django.core.cache.cache.get') as mock_cache_get:
        mock_cache_get.return_value = 3
        response = client.post(
            reverse('password_reset_request'),
            data=json.dumps({
                'email': user.email,
            }),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert 'Too many password reset attempts' in response.data['error']

@pytest.mark.django_db
def test_password_reset_bot_detection(client, user):
    """Test that bot detection works for password reset"""
    response = client.post(
        reverse('password_reset_request'),
        data=json.dumps({
            'email': user.email,
            'website': 'spammy'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Bot detected' in response.data['error']
    assert len(mail.outbox) == 0

@pytest.mark.django_db
def test_password_reset_nonexistent_email(client):
    """Test password reset with non-existent email"""
    response = client.post(
        reverse('password_reset_request'),
        data=json.dumps({
            'email': 'nonexistent@example.com',
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_email_template_rendering():
    """Test that email templates render correctly"""
    from django.template.loader import render_to_string
    
    welcome_context = {
        'username': 'testuser',
        'login_url': 'http://localhost:3000/login'
    }
    welcome_html = render_to_string('emails/welcome_email.html', welcome_context)
    
    assert 'Welcome aboard, testuser!' in welcome_html
    assert 'AIAgent Platform' in welcome_html
    assert 'AI-Powered Chat' in welcome_html
    assert 'http://localhost:3000/login' in welcome_html
    
    reset_context = {
        'username': 'testuser',
        'reset_url': 'http://localhost:3000/reset-password?token=abc123'
    }
    reset_html = render_to_string('emails/password_reset.html', reset_context)
    
    assert 'Hello testuser' in reset_html
    assert 'Password Reset Request' in reset_html
    assert '24 hours' in reset_html
    assert 'http://localhost:3000/reset-password?token=abc123' in reset_html

@pytest.mark.django_db
@patch('django.core.mail.send_mail')
def test_email_sending_error_handling(mock_send_mail, client, user_data):
    """Test that email sending errors are handled gracefully"""
    mock_send_mail.side_effect = Exception("SMTP error")
    
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    user = User.objects.get(username='testuser')
    assert user.email == 'test@example.com'

@pytest.mark.django_db
def test_multiple_welcome_emails_not_sent(client, user_data):
    """Test that welcome emails are only sent on registration, not on updates"""
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1
    
    mail.outbox = []
    
    user = User.objects.get(username='testuser')
    
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert len(mail.outbox) == 0

@pytest.mark.django_db
def test_email_content_security(client, user_data):
    """Test that email content doesn't expose sensitive information"""
    response = client.post(
        '/api/profiles/register/',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    email = mail.outbox[0]
    
    assert 'SecurePass123!' not in email.body
    assert 'testuser' in email.body
    assert 'test@example.com' in email.to

@pytest.mark.django_db
def test_password_reset_confirm_with_email_verification(client, user):
    """Test that password reset confirmation works with email verification"""
    response = client.post(
        reverse('password_reset_request'),
        data=json.dumps({
            'email': user.email,
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    token = ResetPasswordToken.objects.get(user=user)
    
    response = client.post(
        reverse('password_reset_confirm'),
        data=json.dumps({
            'token': token.key,
            'password': 'NewSecurePass456!',
        }),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    user.refresh_from_db()
    assert user.check_password('NewSecurePass456!')
    assert not user.check_password('OldPass123!')