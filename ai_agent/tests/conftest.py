import os
import pytest
from django.contrib.auth.models import User

@pytest.fixture(autouse=True, scope="session")
def set_test_mode_env():
    original = os.environ.get("TEST_MODE")
    os.environ["TEST_MODE"] = "True"
    yield
    if original is not None:
        os.environ["TEST_MODE"] = original
    else:
        del os.environ["TEST_MODE"]

@pytest.fixture
def user(db):
    """
    Fixture to create a user.
    """
    test_user = User.objects.create_user(username='testuser', password='SecurePass123!', email='test@example.com')
    return test_user
