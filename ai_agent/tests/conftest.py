import pytest
from django.contrib.auth.models import User
from django.test import override_settings

@pytest.fixture(autouse=True)
def setup_celery_eager_and_email_backend():
    """
    Ensure Celery tasks run eagerly and emails are captured in tests.
    """
    with override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS=True,
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    ):
        yield

@pytest.fixture
def user(db):
    """
    Fixture to create a user.
    """
    test_user = User.objects.create_user(username='testuser', password='SecurePass123!', email='test@example.com')
    return test_user
