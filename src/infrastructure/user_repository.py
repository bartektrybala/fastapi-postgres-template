from typing import cast

import attr
from sqlalchemy import column, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain import aliases, models
from src.domain.exceptions import map_specific_exception_regex
from src.domain.interface import (
    BaseUserRepository,
    CreateUserRepoDto,
    MissingDbObject,
    UserAlreadyExistsError,
)
from src.infrastructure.sqlalchemy.consts import (
    PSYCOPG_UNIQUE_CONSTRAINT_VIOLATED_ERROR_MESSAGE_REGEX,
)


@attr.s
class UserRepository(BaseUserRepository):
    session: Session = attr.ib()

    @map_specific_exception_regex(
        from_=IntegrityError,
        to=UserAlreadyExistsError,
        from_message=PSYCOPG_UNIQUE_CONSTRAINT_VIOLATED_ERROR_MESSAGE_REGEX.format(
            field="vinted_url"
        ),
        to_message="User with this Vinted URL already exists.",
    )
    def create_user(self, dto: CreateUserRepoDto) -> aliases.UserPk:
        created_user_id = self.session.scalar(
            insert(models.User)
            .values(
                username=dto.username,
            )
            .returning(column("id"))
        )

        assert created_user_id is not None
        return cast(aliases.UserPk, created_user_id)

    def get_users(self) -> list[models.User]:
        return list(
            self.session.scalars(select(models.User).order_by(column("id"))).all()
        )

    def get_by_id(self, id: int) -> models.User:
        user = self.session.scalar(select(models.User).where(column("id") == id))
        if user is None:
            raise MissingDbObject(model=models.User)
        return user
