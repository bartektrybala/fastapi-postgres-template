import typing as t
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, registry

from src.settings import settings


def create_sa_engine() -> t.Generator[Engine]:
    engine = create_engine(
        url=settings.database_url.get_secret_value(),
    )
    try:
        yield engine
    finally:
        engine.dispose()


def get_db_session(engine: Engine) -> Generator[Session]:
    with Session(engine) as session:
        yield session


custom_mapper_registry = registry()
