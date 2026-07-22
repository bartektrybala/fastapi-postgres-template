import typing as t
from collections.abc import Generator

from dependency_injector import containers as c
from dependency_injector import providers as p
from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.auth.jwt_service import JWTTokenService
from src.infrastructure.password_service import PasswordService
from src.infrastructure.sqlalchemy.connection import create_sa_engine, get_db_session
from src.infrastructure.sqlalchemy.tables import map_tables
from src.infrastructure.user_repository import UserRepository


class Container(c.DeclarativeContainer):
    database_engine = p.Resource(create_sa_engine)
    map_tables = p.Factory(map_tables)
    session: p.Provider[Session] = p.Resource(get_db_session, engine=database_engine)

    password_service = p.Factory(PasswordService)
    jwt_service = p.Factory(JWTTokenService)
    user_repository = p.ThreadSafeSingleton(
        UserRepository, session=session, password_service=password_service
    )


container = Container()


def get_container() -> Generator[Container]:
    try:
        yield container
    finally:
        container.reset_singletons()


def get_atomic_container(
    container: t.Annotated[Container, Depends(get_container)],
) -> Generator[Container]:
    try:
        yield container
        container.session().commit()
    except Exception:
        container.session().rollback()
        raise
