import typing as t
import uuid

import attr
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.domain import aliases, models
from src.domain.errors import MissingDbObject
from src.domain.interface import BaseUserRepository, CreateUserRepoDto
from src.tests.factories import UserFactory


@attr.s
class FakeUserRepository(BaseUserRepository):
    user_by_email_collection: dict[str, models.User] = attr.ib(factory=dict)
    user_by_id_collection: dict[aliases.UserPk, models.User] = attr.ib(factory=dict)

    def get_by_email(self, email: str) -> models.User:
        user = self.user_by_email_collection.get(email)
        if user is None:
            raise MissingDbObject(model=models.User)
        return user

    def create_user(self, dto: CreateUserRepoDto) -> aliases.UserPk:
        if dto.email in self.user_by_email_collection:
            raise IntegrityError(
                statement=f"DETAIL:  Key (email)=({dto.email}) already exists.",
                orig=UniqueViolation(
                    f'duplicate key value violates unique constraint "ix_user_email"\nDETAIL:  Key (email)=({dto.email}) already exists.\n'
                ),
                params={
                    "email": dto.email,
                    "city": dto.city,
                    "password_hash": dto.password_hash,
                },
            )

        new_user = UserFactory.build(
            id=uuid.uuid4(),
            email=dto.email,
            password_hash=dto.password_hash,
        )
        self.user_by_email_collection[dto.email] = new_user
        return new_user.id

    def get_by_id(self, id: aliases.UserPk) -> models.User:
        if id not in self.user_by_id_collection:
            raise MissingDbObject(model=models.User)
        return self.user_by_id_collection[id]
