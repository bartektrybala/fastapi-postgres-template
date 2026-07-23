import typing as t
import uuid

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel

from src.containers import Container
from src.domain.auth.current_user import get_current_user
from src.domain.auth.interface import AccesTokenData
from src.domain.models import User
from src.main import app
from src.tests.factories import UserFactory


class DummyUserResponse(BaseModel):
    id: uuid.UUID


@app.get("/dummy/request_user")
def dummy_request_user(
    current_user: t.Annotated[User, Depends(get_current_user)],
) -> DummyUserResponse:
    return DummyUserResponse(id=current_user.id)


@pytest.mark.usefixtures("db")
class TestGetCurrentUserView:
    def test_success(self, api_client: TestClient, container: Container) -> None:
        # given
        user = UserFactory.create()
        token = container.jwt_service().create_access_token(
            data=AccesTokenData(email=user.email)
        )

        # when
        response = api_client.get(
            url="/dummy/request_user",
            headers={"Authorization": f"Bearer {token.access_token}"},
        )

        # then
        assert response.status_code == 200

    def test_invalid_jwt_token(self, api_client: TestClient) -> None:
        # given
        token = "dummy"

        # when
        response = api_client.get(
            url="/dummy/request_user",
            headers={"Authorization": f"Bearer {token}"},
        )

        # then
        assert response.status_code == 401
