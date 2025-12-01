import pytest


@pytest.fixture
def login_path() -> str:
    return "/api/v1/user/login/"


@pytest.fixture
def valid_user_credentials() -> dict:
    return {
        "username": "test",
        "password": "test",
    }


@pytest.fixture
def invalid_user_credentials() -> dict:
    return {
        "username": "wrong",
        "password": "wrong",
    }
