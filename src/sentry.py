import typing as t
from functools import wraps

import sentry_sdk

from src.settings import settings


def init_sentry() -> None:
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            send_default_pii=True,
            enable_logs=True,
        )
