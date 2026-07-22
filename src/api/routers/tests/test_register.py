import pytest
from dirty_equals import IsUUID
from fastapi.testclient import TestClient
from sqlalchemy import column, select

from src.containers import Container
from src.domain import models


@pytest.mark.usefixtures("db")
class TestRegisterView:
    def test_success_register(
        self, api_client: TestClient, container: Container
    ) -> None:
        # given
        session = container.session()

        data = {"email": "test@email.com", "password": "SecurePassword123!"}

        # when
        response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 201
        assert response.json()["id"] == IsUUID()

        id = response.json()["id"]
        user = session.scalar(select(models.User).where(column("id") == id))
        assert user is not None

    def test_user_already_exists(self, api_client: TestClient) -> None:
        # given
        data = {"email": "test@email.com", "password": "SecurePassword123!"}

        # when
        response = api_client.post(url="/register", json=data)
        assert response.status_code == 201
        response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 400
        assert response.json() == {"detail": "User with this email already exists"}
