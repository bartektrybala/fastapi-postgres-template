import inflection
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from src.domain import models
from src.infrastructure.sqlalchemy.connection import custom_mapper_registry
from src.infrastructure.sqlalchemy.consts import DB_TABLE_PREFIX


def map_tables() -> None:
    user_table_name = _create_table_name(model=models.User)
    user_item_table_name = _create_table_name(model=models.UserItem)

    user_table = Table(
        user_table_name,
        custom_mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("username", String(255)),
        Column("vinted_url", Text, unique=True),
    )
    custom_mapper_registry.map_imperatively(models.User, user_table)

    user_item_table = Table(
        user_item_table_name,
        custom_mapper_registry.metadata,
        Column("id", BigInteger, primary_key=True),
        Column("thumbnail_url", Text),
        Column("price", Numeric(10, 2)),
        Column("total_price", Numeric(10, 2)),
        Column("currency_code", String(10)),
        Column("size", String(50)),
        Column("status", String(50)),
        Column("user_id", Integer, ForeignKey(user_table.columns.id)),
    )

    custom_mapper_registry.map_imperatively(
        models.UserItem, user_item_table, properties={"user": relationship(models.User)}
    )


def _create_table_name(model: type[models.BaseModel]) -> str:
    return f"{DB_TABLE_PREFIX}{inflection.tableize(model.__name__)}"
