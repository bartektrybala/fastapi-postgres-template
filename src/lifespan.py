from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import (  # type: ignore[import-untyped]
    AsyncIOScheduler,
)
from apscheduler.triggers.cron import CronTrigger  # type: ignore[import-untyped]
from fastapi import FastAPI

from src.containers import container
from src.domain.vinted.task import fetch_and_store_items


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    container.map_tables()
    container.init_cache()

    container.wire(modules=["src.domain.vinted.task"])
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_store_items, CronTrigger(minute="*/10"))
    scheduler.start()
    yield
    scheduler.shutdown()
    container.reset_singletons()
    container.shutdown_resources()
