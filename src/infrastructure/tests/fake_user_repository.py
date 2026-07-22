import attr
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.domain import aliases, models
from src.domain.exceptions import MissingDbObject
from src.domain.interface import BaseUserRepository
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

    def create_user(self, email: str, password: str) -> aliases.UserPk:
        if email in self.user_by_email_collection:
            raise IntegrityError(
                statement=f"DETAIL:  Key (email)=({email}) already exists.",
                orig=UniqueViolation(
                    f'duplicate key value violates unique constraint "ix_user_email"\nDETAIL:  Key (email)=({email}) already exists.\n'  # noqa: E501
                ),
                params={
                    "email": email,
                },
            )

        new_user = UserFactory.build(
            email=email,
        )
        self.user_by_email_collection[email] = new_user
        return new_user.id

    def get_by_id(self, id: aliases.UserPk) -> models.User:
        if id not in self.user_by_id_collection:
            raise MissingDbObject(model=models.User)
        return self.user_by_id_collection[id]
