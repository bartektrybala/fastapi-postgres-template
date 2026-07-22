from typing import Generic, TypeVar

import factory
import faker

from src.domain import models

T = TypeVar("T")

fake = faker.Faker()


class BaseFactory(Generic[T], factory.Factory[T]):
    pass


class BaseSQLAlchemyFactory(
    BaseFactory[T],
    factory.alchemy.SQLAlchemyModelFactory,  # type: ignore[type-arg]
):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_FLUSH


class UserFactory(BaseSQLAlchemyFactory[models.User]):
    class Meta:
        model = models.User

    id = factory.Sequence(lambda n: n + 1)
    username = factory.LazyFunction(fake.user_name)
