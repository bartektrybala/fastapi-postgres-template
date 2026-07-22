import inflection
from sqlalchemy import (
    Column,
    String,
    Table,
)
from sqlalchemy.types import UUID

from src.domain import models
from src.infrastructure.sqlalchemy.connection import custom_mapper_registry
from src.infrastructure.sqlalchemy.consts import DB_TABLE_PREFIX


def map_tables() -> None:
    user_table_name = _create_table_name(model=models.User)

    user_table = Table(
        user_table_name,
        custom_mapper_registry.metadata,
        Column("id", UUID, primary_key=True),
        Column("email", String(255), unique=True, index=True),
        Column("password_hash", String(60)),
    )
    custom_mapper_registry.map_imperatively(models.User, user_table)


def _create_table_name(model: type[models.BaseModel]) -> str:
    return f"{DB_TABLE_PREFIX}{inflection.tableize(model.__name__)}"
