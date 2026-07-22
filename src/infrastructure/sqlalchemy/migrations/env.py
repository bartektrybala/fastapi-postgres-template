from logging.config import fileConfig

import alembic
from sqlalchemy import engine_from_config, pool

from src.infrastructure.sqlalchemy.connection import custom_mapper_registry
from src.infrastructure.sqlalchemy.tables import map_tables
from src.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = alembic.context.config

config.set_main_option("sqlalchemy.url", settings.database_url.get_secret_value())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = custom_mapper_registry.metadata


def include_name(
    name: str | None,
    type_: str | None,
    parent_names: list[str] | None,  # noqa: ARG001
) -> bool:
    """Ignore existing tables (necessary to ignore saleor tables)"""
    if type_ == "table":
        return name in target_metadata.tables
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    alembic.context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_name=include_name,
        dialect_opts={"paramstyle": "named"},
    )

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        map_tables()
        alembic.context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()
        connection.commit()


if alembic.context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
