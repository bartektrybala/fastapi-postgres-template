from datetime import UTC, datetime, timedelta

import jwt
from pydantic import ValidationError

from src.domain.auth.exceptions import InvalidAuthToken
from src.domain.auth.interface import AccesTokenData, TokenPayload
from src.domain.auth.interface import Token as JWTToken
from src.settings import settings


class JWTTokenService:
    def create_access_token(self, data: AccesTokenData) -> JWTToken:
        exp = datetime.now(tz=UTC) + timedelta(
            seconds=settings.jwt_access_token_expires_in_seconds
        )
        payload = TokenPayload(exp=exp, email=data.email)

        encoded_jwt = jwt.encode(
            payload=payload.model_dump(),
            key=settings.jwt_secret_key.get_secret_value(),
            algorithm=settings.jwt_hashing_alg,
        )
        return JWTToken(access_token=encoded_jwt)

    def validate_access_token(self, token: str) -> AccesTokenData:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.jwt_secret_key.get_secret_value(),
                algorithms=[settings.jwt_hashing_alg],
            )
        except (
            jwt.InvalidAlgorithmError,
            jwt.InvalidSignatureError,
            jwt.DecodeError,
            jwt.ExpiredSignatureError,
        ):
            raise InvalidAuthToken

        try:
            payload = TokenPayload.model_validate(payload)
        except ValidationError:
            raise InvalidAuthToken

        return AccesTokenData(email=payload.email)
