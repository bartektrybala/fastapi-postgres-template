import typing as t
from unittest import mock

import pytest
from dependency_injector import providers as p
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from src.containers import Container
from src.containers import container as container_obj
from src.infrastructure.sqlalchemy.connection import custom_mapper_registry
from tests.factories import BaseSQLAlchemyFactory


def _set_session_on_factory_child_classes(  # type: ignore[explicit-any]
    session: Session,
    factory: type[BaseSQLAlchemyFactory[t.Any]],
) -> None:
    for child in factory.__subclasses__():
        child._meta.sqlalchemy_session = session  # type: ignore[attr-defined] # noqa: SLF001
        _set_session_on_factory_child_classes(session, child)


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    return container_obj.database_engine()


@pytest.fixture(scope="session")
def setup_database(db_engine: Engine) -> t.Generator[None]:
    if not database_exists(url=db_engine.url):
        create_database(url=db_engine.url)

    container_obj.map_tables()
    custom_mapper_registry.metadata.create_all(db_engine)
    yield
    custom_mapper_registry.metadata.drop_all(db_engine)


@pytest.fixture
def db(
    setup_database: None,  # noqa: ARG001
    db_engine: Engine,
) -> t.Generator[Session]:
    connection = db_engine.connect()
    transaction = connection.begin()
    connection.begin_nested()
    session = Session(connection, expire_on_commit=False, autoflush=False)

    container_obj.session.override(p.Object(session))
    _set_session_on_factory_child_classes(session, BaseSQLAlchemyFactory)

    try:
        yield session
    finally:
        if connection.in_transaction():
            transaction.rollback()
        connection.close()




@pytest.fixture
def container() -> t.Generator[Container]:
    yield container_obj
    container_obj.reset_override()
    container_obj.reset_singletons()
    container_obj.shutdown_resources()
