import os
import pathlib
import typing as t

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.consts import DAY_IN_SECONDS

EnvType = t.Literal["development", "production", "test"]
ENV = t.cast("EnvType", os.getenv("ENV", "development"))

BASE_DIR = pathlib.Path(__file__).parent
ENV_FILE_PATH = BASE_DIR / "env" / f".env.{ENV}"


class Settings(BaseSettings):
    env: EnvType = ENV
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")

    database_url: SecretStr
    jwt_secret_key: SecretStr

    allowed_origins: list[str]
    sentry_dsn: str | None = None
    excluded_logging_endpoints: list[str] = ["/health"]

    jwt_access_token_expires_in_seconds: int = 5 * DAY_IN_SECONDS
    jwt_hashing_alg: str = "HS256"


settings = Settings()  # type: ignore[call-arg]


__all__ = ["BASE_DIR", "ENV", "ENV_FILE_PATH", "Settings", "settings"]
