import uuid
from typing import TypeVar

import factory
import faker
from factory.alchemy import SQLAlchemyOptions
from sqlalchemy.orm.session import Session

from src.domain import models

T = TypeVar("T", bound=models.BaseModel)

fake = faker.Faker()


class TypedSQLAlchemyOptions(SQLAlchemyOptions):
    sqlalchemy_session: Session | None


class BaseSQLAlchemyFactory(
    factory.alchemy.SQLAlchemyModelFactory, factory.base.BaseFactory[T]
):
    _meta: TypedSQLAlchemyOptions

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_FLUSH


PLAIN_PASSWORD = "password"
HASH_OF_PLAIN_PASSWORD = "$2b$12$vKSqBNic7dfU7zCh1MhEDOoTKCfh3yP6impFzEOSQAq8BD8Q4VExu"


class UserFactory(BaseSQLAlchemyFactory[models.User]):
    class Meta:
        model = models.User

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.LazyFunction(fake.email)
    password_hash = HASH_OF_PLAIN_PASSWORD
