import uuid

import attr
from sqlalchemy import column, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain import aliases, models
from src.domain.exceptions import (
    MissingDbObject,
    UserAlreadyExists,
    map_specific_exception_regex,
)
from src.domain.interface import (
    BaseUserRepository,
)
from src.infrastructure.password_service import PasswordService
from src.infrastructure.sqlalchemy.consts import (
    PSYCOPG_UNIQUE_CONSTRAINT_VIOLATED_ERROR_MESSAGE_REGEX,
)


@attr.s
class UserRepository(BaseUserRepository):
    session: Session = attr.ib()
    password_service: PasswordService = attr.ib()

    @map_specific_exception_regex(
        from_=IntegrityError,
        to=UserAlreadyExists,
        from_message=PSYCOPG_UNIQUE_CONSTRAINT_VIOLATED_ERROR_MESSAGE_REGEX.format(
            field="email"
        ),
        to_message="User with this email already exists.",
    )
    def create_user(self, email: str, password: str) -> aliases.UserPk:
        user_id = aliases.UserPk(uuid.uuid4())
        password_hash = self.password_service.hash(password)

        user = models.User(
            id=user_id,
            email=email,
            password_hash=password_hash,
        )
        self.session.add(user)
        return user_id

    def get_users(self) -> list[models.User]:
        return list(
            self.session.scalars(select(models.User).order_by(column("id"))).all()
        )

    def get_by_id(self, id: aliases.UserPk) -> models.User:
        user = self.session.scalar(select(models.User).where(column("id") == id))
        if user is None:
            raise MissingDbObject(model=models.User)
        return user
