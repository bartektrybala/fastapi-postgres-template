import abc

import attr

from src.domain import aliases


@attr.s
class BaseModel(abc.ABC): ...


@attr.s
class User(BaseModel):
    id: aliases.UserPk = attr.ib()
    username: str = attr.ib()
