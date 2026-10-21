import typing as t

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import registry

from src.settings import settings


def create_sa_engine() -> t.Generator[Engine]:
    engine = create_engine(
        url=settings.database_url.get_secret_value(),
    )
    try:
        yield engine
    finally:
        engine.dispose()


custom_mapper_registry = registry()
