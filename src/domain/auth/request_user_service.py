import attr

from src.domain.auth.exceptions import CurrentUserInvalidCredentials, InvalidAuthToken
from src.domain.auth.jwt_service import JWTTokenService
from src.domain.exceptions import MissingDbObject
from src.domain.models import User
from src.infrastructure.user_repository import UserRepository


@attr.s
class RequestUserService:
    jwt_token_service: JWTTokenService = attr.ib()
    user_repository: UserRepository = attr.ib()

    def get_current_user(self, token: str) -> User:
        try:
            access_token_data = self.jwt_token_service.validate_access_token(
                token=token
            )
            user = self.user_repository.get_by_email(email=access_token_data.email)
        except (InvalidAuthToken, MissingDbObject):
            raise CurrentUserInvalidCredentials
        return user
