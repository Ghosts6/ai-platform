import os
import pytest
from django.conf import settings

@pytest.fixture(scope="session", autouse=True)
def set_sqlite_db_for_tests():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": False,
    }

@pytest.fixture(autouse=True, scope="session")
def set_test_mode_env():
    original = os.environ.get("TEST_MODE")
    os.environ["TEST_MODE"] = "True"
    yield
    if original is not None:
        os.environ["TEST_MODE"] = original
    else:
        del os.environ["TEST_MODE"]