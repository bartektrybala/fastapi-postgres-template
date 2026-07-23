import pytest
from sqlalchemy import column, select

from src.containers import Container
from src.domain import models
from src.domain.exceptions import (
    MissingDbObject,
    UserAlreadyExists,
)
from src.tests.factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUserRepository:
    def test_create_user(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        session = container.session()

        # when
        created_user_id = repository.create_user(
            email="test@email.com", password="SecurePassword123!"
        )

        # then
        user = session.scalar(
            select(models.User).where(column("id") == created_user_id)
        )
        assert user is not None

    def test_create_user_already_exists(self, container: Container) -> None:
        # given
        repository = container.user_repository()

        email = "test@email.com"
        repository.create_user(email=email, password="SecurePassword123!")

        # when & then
        with pytest.raises(
            UserAlreadyExists, match="User with this email already exists."
        ):
            repository.create_user(email=email, password="SecurePassword123!")

    def test_get_users(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        UserFactory.create_batch(3)

        # when
        users = repository.get_users()

        # then
        assert len(users) == 3
        assert all(isinstance(u, models.User) for u in users)

    def test_user_by_id(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        user_ = UserFactory.create()

        # when
        user = repository.get_by_id(id=user_.id)

        # then
        assert user.id == user_.id

    def test_get_by_id_missing_user(self, container: Container) -> None:
        # given
        user = UserFactory.build()
        repository = container.user_repository()

        # when & then
        with pytest.raises(MissingDbObject, match="User"):
            repository.get_by_id(id=user.id)

    def test_user_by_email(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        user_ = UserFactory.create()

        # when
        user = repository.get_by_email(email=user_.email)

        # then
        assert user.id == user_.id

    def test_get_by_email_missing_user(self, container: Container) -> None:
        # given
        user = UserFactory.build()
        repository = container.user_repository()

        # when & then
        with pytest.raises(MissingDbObject, match="User"):
            repository.get_by_email(email=user.email)
