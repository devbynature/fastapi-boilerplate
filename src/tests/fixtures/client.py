import pytest
from starlette.testclient import TestClient

from core.main import app


@pytest.fixture
def client():
    with TestClient(
        app=app,
    ) as c:
        yield c
