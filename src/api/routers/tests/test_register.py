import pytest
from fastapi.testclient import TestClient
from tests.infrastructure.db.fake_repository import FakeUserRepository

from src.containers import Container, container
from src.domain import models
from src.tests.factories import UserFactory
from tests import matchers


class TestRegisterView:
    @pytest.mark.usefixtures("db")
    def test_success_register(
        self, api_client: TestClient, container: Container
    ) -> None:
        # given
        user_repository = container.user_repository()

        data = {
            "email": "new@email.com",
            "password": "strong_password11",
        }

        # when
        response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 201
        assert response.json() == {
            "id": matchers.Any(str),
            "email": data["email"],
        }

        user = user_repository.get_by_id(id=response.json()["id"])
        assert isinstance(user, models.User)

    def test_user_already_exists(self, api_client: TestClient) -> None:
        # given
        user = UserFactory.build()
        data = {
            "email": user.email,
            "city": user.city.value,
            "password": "strong_password11",
        }

        # when
        with container.user_repository.override(
            FakeUserRepository(user_by_email_collection={user.email: user})
        ):
            response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 400
        assert response.json() == {"detail": "User with this email already exists"}
