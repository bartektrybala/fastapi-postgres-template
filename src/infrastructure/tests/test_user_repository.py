import pytest
from sqlalchemy import column, select

from src.containers import Container
from src.domain import models
from src.domain.consts import USER_SZYMEK_ID
from src.domain.interface import (
    CreateUserRepoDto,
    MissingDbObject,
    UserAlreadyExistsError,
)
from tests.factories import UserFactory


class TestUserRepository:
    @pytest.mark.usefixtures("db")
    def test_create_user(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        session = container.session()

        dto = CreateUserRepoDto(
            username="szymiitrybala",
            vinted_url=f"https://www.vinted.pl/member/{USER_SZYMEK_ID}",
        )

        # when
        created_user_id = repository.create_user(dto=dto)

        # then
        user = session.scalar(
            select(models.User).where(column("id") == created_user_id)
        )
        assert user is not None

    @pytest.mark.usefixtures("db")
    def test_create_user_already_exists(self, container: Container) -> None:
        # given
        repository = container.user_repository()

        data = {
            "username": "szymiitrybala",
            "vinted_url": f"https://www.vinted.pl/member/{USER_SZYMEK_ID}",
        }
        repository.create_user(dto=CreateUserRepoDto(**data))

        # when & then
        with pytest.raises(
            UserAlreadyExistsError, match="User with this Vinted URL already exists."
        ):
            repository.create_user(
                dto=CreateUserRepoDto(
                    username="another_username",
                )
            )

    @pytest.mark.usefixtures("db")
    def test_get_users(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        UserFactory.create_batch(3)

        # when
        users = repository.get_users()

        # then
        assert len(users) == 3
        assert all(isinstance(u, models.User) for u in users)

    @pytest.mark.usefixtures("db")
    def test_user_by_id(self, container: Container) -> None:
        # given
        repository = container.user_repository()
        user_ = UserFactory.create()

        # when
        user = repository.get_by_id(id=user_.id)

        # then
        assert user.id == user_.id

    @pytest.mark.usefixtures("db")
    def test_get_by_id_missing_user(self, container: Container) -> None:
        # given
        user = UserFactory.build()
        repository = container.user_repository()

        # when & then
        with pytest.raises(MissingDbObject, match="User"):
            repository.get_by_id(id=user.id)
