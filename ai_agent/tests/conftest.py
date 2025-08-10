import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def set_test_mode_env():
    original = os.environ.get("TEST_MODE")
    os.environ["TEST_MODE"] = "True"
    yield
    if original is not None:
        os.environ["TEST_MODE"] = original
    else:
        del os.environ["TEST_MODE"]