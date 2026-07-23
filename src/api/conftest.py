import typing as t

import pytest
from fastapi.testclient import TestClient

from src.domain import models
from src.domain.auth.current_user import get_current_user
from src.main import app
from src.tests.factories import UserFactory


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def user() -> models.User:
    return UserFactory.create()


@pytest.fixture
def user_client(api_client: TestClient, user: models.User) -> t.Generator[TestClient]:
    app.dependency_overrides[get_current_user] = lambda: user
    yield api_client
    app.dependency_overrides.clear()
