import pytest
from fastapi.testclient import TestClient

from src.api.consts import API_KEY_NAME
from src.main import app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(
        app=app,
        headers={API_KEY_NAME: "dummy"},
    )
