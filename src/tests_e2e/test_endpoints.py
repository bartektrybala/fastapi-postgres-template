import typing as t

import pytest
import requests
from dirty_equals import IsStr
from sqlalchemy.orm import Session

from src.domain import models
from src.tests.factories import PLAIN_PASSWORD, UserFactory

API_BASE_URL = "http://localhost/api"


@pytest.fixture
def user(db_session: Session) -> models.User:
    user = UserFactory.create()
    db_session.connection().commit()
    return user


@pytest.fixture
def access_token(user: models.User) -> str:
    response = requests.post(
        url=f"{API_BASE_URL}/login",
        json={"email": user.email, "password": PLAIN_PASSWORD},
    )
    assert response.status_code == 200
    return t.cast(str, response.json()["access_token"])


@pytest.mark.integration
@pytest.mark.usefixtures("clear_db")
class TestUserEndpoints:
    def test_user_register(self, db_session: Session) -> None:
        # given
        data = {
            "email": "tomek@email.com",
            "password": "strong_password123",
        }

        assert db_session.query(models.User).count() == 0

        # when
        response = requests.post(
            url=f"{API_BASE_URL}/register",
            json=data,
        )

        # then
        assert response.status_code == 201
        assert db_session.query(models.User).count() == 1

    def test_user_login(self, user: models.User) -> None:
        # given
        data = {
            "email": user.email,
            "password": PLAIN_PASSWORD,
        }

        # when
        response = requests.post(
            url=f"{API_BASE_URL}/login",
            json=data,
        )

        # then
        assert response.status_code == 200
        assert response.json() == {
            "access_token": IsStr(),
            "token_type": "bearer",
        }

    def test_user_me(self, access_token: str, user: models.User) -> None:
        # when
        response = requests.get(
            url=f"{API_BASE_URL}/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # then
        assert response.status_code == 200
        assert response.json() == {
            "id": str(user.id),
            "email": user.email,
        }
