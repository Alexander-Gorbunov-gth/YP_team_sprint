from logging import config as logging_config
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


# class Settings(BaseSettings):
#     # project_name: str = Field('movies', validation_alias='PROJECT_NAME')
#
#     # redis_host: str = Field('127.0.0.1', validation_alias='REDIS_HOST')
#     # redis_port: int = Field(6379, validation_alias='REDIS_PORT')
#     # redis_password: SecretStr | None = Field(None, validation_alias='REDIS_PASSWORD')
#
#     model_config = SettingsConfigDict(
#         env_file=".auth.env", env_file_encoding="utf-8", extra="ignore"
#     )
#     debug: bool
#     redis_url: str = "redis://localhost:6379"
#     db_url: str
#     secret_key_jwt: str
#
#     # @property
#     # def redis_url(self) -> str:
#     #     """Формируем URL для подключения к Redis"""
#     #     return f'http://{self.redis_host}:{self.redis_port}'
#
#
# settings = Settings()


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".auth.env"),
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
