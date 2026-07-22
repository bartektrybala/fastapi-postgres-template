import pytest
from fastapi.testclient import TestClient
from sqlalchemy import column, select

from src.containers import Container
from src.domain import models
from src.domain.interface import CreateUserRepoDto
from tests import matchers


class TestRegisterView:
    @pytest.mark.usefixtures("db")
    def test_success_register(
        self, api_client: TestClient, container: Container
    ) -> None:
        # given
        session = container.session()

        data = {
            "vinted_url": f"https://www.vinted.pl/member/{USER_SZYMEK_ID}",
            "username": "szymiitrybala",
        }

        # when
        response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 201
        assert response.json() == {"id": matchers.Any(int), **data}

        user = session.scalar(
            select(models.User).where(column("id") == response.json()["id"])
        )
        assert user is not None
        assert user.vinted_url == data["vinted_url"]

    @pytest.mark.usefixtures("db")
    def test_user_already_exists(
        self, api_client: TestClient, container: Container
    ) -> None:
        # given
        user_repository = container.user_repository()

        data = {
            "vinted_url": f"https://www.vinted.pl/member/{USER_SZYMEK_ID}",
            "username": "szymiitrybala",
        }
        user_repository.create_user(
            dto=CreateUserRepoDto(
                vinted_url=data["vinted_url"], username=data["username"]
            )
        )

        # when
        response = api_client.post(url="/register", json=data)

        # then
        assert response.status_code == 400
        assert response.json() == {
            "detail": "User with this Vinted URL already exists."
        }
