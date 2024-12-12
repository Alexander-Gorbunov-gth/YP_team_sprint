from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".auth.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AuthSettings(ModelConfig):
    secret_key_jwt: str
    algorythm_jwt: str
    # db_echo: bool = False
    db_echo: bool = True
    debug: bool = False


class PostgresSettings(ModelConfig):
    postgres_host: str = ...
    postgres_user: str = ...
    postgres_password: str = ...
    postgres_db: str = ...

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:5432/"
            f"{self.postgres_db}"
        )
    
    @property
    def db_sync_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:5432/"
            f"{self.postgres_db}"
        )


class RedisSettings(ModelConfig):
    redis_host: str = ...
    redis_port: str = ...

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings: Settings = Settings()
