from logging import config as logging_config
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    project_name: str = Field("movies", validation_alias="PROJECT_NAME")

    elastic_host: str = Field("127.0.0.1", validation_alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, validation_alias="ELASTIC_PORT")

    redis_host: str = Field("127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: int = Field(6379, validation_alias="REDIS_PORT")
    redis_password: SecretStr | None = Field(None, validation_alias="REDIS_PASSWORD")

    jwt_secret_key: str = Field("secret", validation_alias="SECRET_KEY")
    jwt_alg: str = Field("HS256", validation_alias="JWT_ALGORITHM")

    rate_window: int = Field(60, validation_alias="RATE_WINDOW")
    rate_limit: int = Field(100, validation_alias="RATE_LIMIT")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def elastic_url(self) -> str:
        """Формируем URL для подключения к Elasticsearch."""
        return f"http://{self.elastic_host}:{self.elastic_port}"

    @property
    def redis_url(self) -> str:
        """Формируем URL для подключения к Redis"""
        return f"http://{self.redis_host}:{self.redis_port}"


settings = Settings()
