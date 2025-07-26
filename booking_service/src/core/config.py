import logging
import logging.config
import os
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import get_logger_settings


def init_logger():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    LOGS_DIR = BASE_DIR / "logs"

    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)

    logging.config.dictConfig(get_logger_settings(LOGS_DIR))


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env",), extra="ignore")


class PostgresSettings(ModelConfig):
    """Настройки Postgres"""

    host: str = Field(default="127.0.0.1", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    db_name: str = Field(default="booking_db", validation_alias="POSTGRES_DB")
    user: str = Field(default="booking_user", validation_alias="POSTGRES_USER")
    password: SecretStr = Field(..., validation_alias="POSTGRES_PASSWORD")
    echo: bool = Field(default=False, validation_alias="POSTGRES_ECHO")

    @property
    def connection_url(self) -> str:
        """Ссылка для подключения с драйвером asyncpg"""

        pwd = self.password.get_secret_value()
        return f"postgresql+asyncpg://{self.user}:{pwd}@{self.host}:{self.port}/{self.db_name}"

    @property
    def alembic_url(self) -> str:
        """Ссылка для подключения с драйвером psycopg2"""

        pwd = self.password.get_secret_value()
        return f"postgresql+psycopg2://{self.user}:{pwd}@{self.host}:{self.port}/{self.db_name}"


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()


init_logger()

settings = Settings()
