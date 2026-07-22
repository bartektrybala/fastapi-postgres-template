from datetime import UTC, datetime, timedelta

import jwt
import pytest
import time_machine
from jwt.exceptions import InvalidTokenError

from src.containers import Container
from src.domain.auth.interface import AccesTokenData, TokenPayload
from src.domain.auth.interface import Token as JWTToken
from src.settings import settings


class TestJWTTokenService:
    def test_create_token(self, container: Container) -> None:
        # given
        service = container.jwt_service()
        email = "test@email.com"

        # when
        token = service.create_access_token(data=AccesTokenData(email=email))

        # then
        assert isinstance(token, JWTToken)

    def test_validate_token(self, container: Container) -> None:
        # given
        service = container.jwt_service()
        email = "test@email.com"

        # when
        token = service.create_access_token(data=AccesTokenData(email=email))
        access_token_data = service.validate_access_token(token=token.access_token)

        # then
        assert access_token_data == AccesTokenData(email=email)

    def test_expired_token(self, container: Container) -> None:
        # given
        service = container.jwt_service()
        email = "test@email.com"

        # when & then
        token = service.create_access_token(data=AccesTokenData(email=email))
        expired = timedelta(seconds=settings.jwt_access_token_expires_in_seconds + 1)
        with time_machine.travel(expired), pytest.raises(InvalidTokenError):
            service.validate_access_token(token=token.access_token)

    def test_invalid_token(self, container: Container) -> None:
        # given
        service = container.jwt_service()
        invalid_token = "dummy_token"

        # when
        with pytest.raises(InvalidTokenError):
            service.validate_access_token(token=invalid_token)

    def test_invalid_secret_key(self, container: Container) -> None:
        # given
        service = container.jwt_service()

        payload = TokenPayload(
            exp=datetime.now(tz=UTC) + timedelta(days=1),
            email="test@email.com",
        )
        invalid_token = jwt.encode(
            payload=payload.model_dump(),
            key="invalid_key",
            algorithm=settings.jwt_hashing_alg,
        )

        # when
        with pytest.raises(InvalidTokenError):
            service.validate_access_token(token=invalid_token)

    def test_invalid_algorithm(self, container: Container) -> None:
        # given
        service = container.jwt_service()

        payload = TokenPayload(
            exp=datetime.now(tz=UTC) + timedelta(days=1),
            email="test@email.com",
        )
        invalid_token = jwt.encode(
            payload=payload.model_dump(),
            key=settings.jwt_secret_key.get_secret_value(),
            algorithm="HS512",
        )

        # when
        with pytest.raises(InvalidTokenError):
            service.validate_access_token(token=invalid_token)

    def test_invalid_payload(self, container: Container) -> None:
        # given
        service = container.jwt_service()

        invalid_payload = {"dummy": "dummy"}
        token = jwt.encode(
            payload=invalid_payload,
            key=settings.jwt_secret_key.get_secret_value(),
            algorithm=settings.jwt_hashing_alg,
        )

        # when
        with pytest.raises(InvalidTokenError):
            service.validate_access_token(token=token)
