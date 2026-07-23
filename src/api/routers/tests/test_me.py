import pytest
from fastapi.testclient import TestClient

from src.domain.models import User


class TestMeView:
    @pytest.mark.usefixtures("db")
    def test_success_get(self, user_client: TestClient, user: User) -> None:
        # when
        response = user_client.get(url="/user/me")

        # then
        assert response.status_code == 200
        assert response.json() == {
            "id": str(user.id),
            "email": user.email,
        }
