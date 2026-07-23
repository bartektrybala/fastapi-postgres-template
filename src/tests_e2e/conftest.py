import typing as t

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from src.conftest import _set_session_on_factory_child_classes
from src.domain import models
from src.infrastructure.sqlalchemy.tables import map_tables
from src.tests.factories import BaseSQLAlchemyFactory


@pytest.fixture(scope="session")
def db_engine() -> t.Generator[Engine]:
    engine = create_engine(url="postgresql://postgres:password@localhost/e2e_testing")
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def setup_database(db_engine: Engine) -> None:
    if not database_exists(url=db_engine.url):
        create_database(url=db_engine.url)


@pytest.fixture(scope="session")
def db_session(
    setup_database: None,  # noqa: ARG001
    db_engine: Engine,
) -> t.Generator[Session]:
    connection = db_engine.connect()
    connection.begin_nested()
    session = Session(connection, expire_on_commit=False, autoflush=False)
    map_tables()
    _set_session_on_factory_child_classes(session, BaseSQLAlchemyFactory)

    try:
        yield session
    finally:
        connection.close()


@pytest.fixture
def clear_db(db_session: Session) -> t.Generator[None]:
    yield
    db_session.query(models.User).delete()
    db_session.connection().commit()
