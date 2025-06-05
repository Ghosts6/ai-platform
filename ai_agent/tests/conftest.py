import os
import pytest
from django.conf import settings

@pytest.fixture(scope="session", autouse=True)
def set_sqlite_db_for_tests():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }