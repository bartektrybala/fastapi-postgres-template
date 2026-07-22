import abc
from dataclasses import dataclass
from typing import Generic, TypeVar

from src.domain import aliases, models


@dataclass
class CreateUserRepoDto:
    username: str


class UserAlreadyExistsError(Exception):
    pass


Model = TypeVar("Model", bound=type[object])


class MissingDbObject(Generic[Model], Exception):
    def __init__(self, model: Model):
        self.model = model
        super().__init__(f"Missing object of type {model.__name__}")


class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_user(self, dto: CreateUserRepoDto) -> aliases.UserPk:
        pass

    @abc.abstractmethod
    def get_users(self) -> list[models.User]:
        pass

    @abc.abstractmethod
    def get_by_id(self, id: aliases.UserPk) -> models.User:
        pass
