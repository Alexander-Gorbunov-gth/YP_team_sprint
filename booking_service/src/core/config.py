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


class RabbitSettings(ModelConfig):
    """
    Настройки для RabbitMQ
    host: Хост RabbitMQ (по умолчанию localhost)
    port: Порт RabbitMQ (по умолчанию 5672)
    user: Пользователь RabbitMQ (по умолчанию guest)
    password: Пароль RabbitMQ (по умолчанию guest)
    exchange_name: Имя обменника (по умолчанию notifications)
    router_queue_title: Имя очереди для роутера (по умолчанию router_queue)
    email_queue_title: Имя очереди для email (по умолчанию email_queue)
    push_queue_title: Имя очереди для push (по умолчанию push_queue)
    """

    host: str = Field("localhost", validation_alias="RABBIT_HOST")
    port: int = Field(5672, validation_alias="RABBIT_PORT")
    user: str = Field("user", validation_alias="RABBITMQ_DEFAULT_USER")
    password: SecretStr = Field("password", validation_alias="RABBITMQ_DEFAULT_PASS")
    exchange_name: str = Field("notifications", validation_alias="RABBIT_EXCHANGE_NAME")
    max_retry_count: int = Field(3, validation_alias="RABBIT_MAX_RETRY_COUNT", ge=0, le=10)
    router_queue_title: str = Field("router_queue", validation_alias="RABBIT_ROUTER_QUEUE_TITLE")
    email_queue_title: str = Field("email_queue", validation_alias="RABBIT_EMAIL_QUEUE_TITLE")
    push_queue_title: str = Field("push_queue", validation_alias="RABBIT_PUSH_QUEUE_TITLE")
    dlq_ttl: int = Field(60000, validation_alias="RABBIT_DLQ_TTL", ge=0, le=3600000)

    @property
    def connection_url(self) -> str:
        """
        Формирует URL для подключения к RabbitMQ
        """
        return f"amqp://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/"


class AuthSettings(ModelConfig):
    """Настройки авторизации"""

    secret_key: SecretStr = Field(..., validation_alias="AUTH_SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="AUTH_ALGORITHM")


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    rabbit: RabbitSettings = RabbitSettings()
    auth: AuthSettings = AuthSettings()


init_logger()

settings = Settings()
