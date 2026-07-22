import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health import router as health_router
from src.api.routers.profile import router as profile_router
from src.api.routers.sync import router as sync_router
from src.api.routers.register import router as user_router
from src.lifespan import lifespan
from src.logs import EndpointFilter
from src.sentry import init_sentry
from src.settings import BASE_DIR, settings

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=health_router)
app.include_router(router=user_router)
app.include_router(router=profile_router)
app.include_router(router=sync_router)

init_sentry()


logging.getLogger("uvicorn.access").addFilter(
    EndpointFilter(excluded_endpoints=settings.excluded_logging_endpoints)
)
