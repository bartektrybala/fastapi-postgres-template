import abc

from src.domain import aliases, models


class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_user(self, email: str, password: str) -> aliases.UserPk:
        pass

    @abc.abstractmethod
    def get_users(self) -> list[models.User]:
        pass

    @abc.abstractmethod
    def get_by_id(self, id: aliases.UserPk) -> models.User:
        pass
