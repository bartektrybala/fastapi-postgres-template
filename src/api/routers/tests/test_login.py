import pytest
from dirty_equals import IsStr
from fastapi.testclient import TestClient

from src.containers import Container
from src.tests.factories import UserFactory


@pytest.mark.usefixtures("db")
class TestLoginView:
    def test_success_login(self, api_client: TestClient, container: Container) -> None:
        # given
        request_user_service = container.request_user_service()
        user = UserFactory.create(email="user@email.com")

        # when
        response = api_client.post(
            url="/login",
            json={"email": user.email, "password": "password"},
        )

        # then
        assert response.status_code == 200
        response_json = response.json()
        assert response_json == {
            "access_token": IsStr(),
            "token_type": "bearer",
        }

        user_from_token = request_user_service.get_current_user(
            token=response_json["access_token"]
        )
        assert user_from_token.id == user.id

    def test_missing_user(self, api_client: TestClient) -> None:
        # given
        user = UserFactory.create(email="user@email.com")

        # when
        response = api_client.post(
            url="/login",
            json={"email": user.email, "password": "invalid"},
        )

        # then
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect email or password"}

    def test_invalid_password(self, api_client: TestClient) -> None:
        # when
        response = api_client.post(
            url="/login",
            json={"email": "missing-user@email.com", "password": "password"},
        )

        # then
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect email or password"}
