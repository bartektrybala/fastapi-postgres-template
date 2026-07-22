from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.containers import container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    container.map_tables()

    yield
    container.reset_singletons()
    container.shutdown_resources()
