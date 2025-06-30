import logging
import os
from pathlib import Path
from typing import ClassVar

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.logger import get_logger_settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

logging.config.dictConfig(get_logger_settings(LOGS_DIR))


class ModelConfig(BaseSettings):
    env_file_name: ClassVar[str] = os.getenv("ENVIRONMENT", "dev")
    model_config = SettingsConfigDict(
        env_file=(".env") if env_file_name != "prod" else (".env, ../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ProjectSettings(ModelConfig):
    """
    Настройки для проекта
    title: Название проекта (по умолчанию User activity service)
    decription: Описание проекта (по умолчанию "")
    debug: Флаг для включения режима отладки (по умолчанию False)
    """

    title: str = Field("User activity service", validation_alias="PROJECT_TITLE")
    description: str = Field("", validation_alias="PROJECT_DESCRIPTION")
    debug: bool = Field(False, validation_alias="DEBUG")
    use_mock_data: bool = Field(True, validation_alias="USE_MOCK_DATA")


class AuthSettings(ModelConfig):
    """
    Настройки для сервиса авторизации
    auth_service_url: Ссылка на сервис авторизации (по умолчанию None)
    auth_token: Токен для авторизации (по умолчанию None)
    """

    service_url: str | None = Field(
        "http://auth_service:8001", validation_alias="AUTH_SERVICE_URL"
    )
    token: str | None = Field("some_token", validation_alias="AUTH_TOKEN")


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
    max_retry_count: int = Field(
        3, validation_alias="RABBIT_MAX_RETRY_COUNT", ge=0, le=10
    )
    router_queue_title: str = Field(
        "router_queue", validation_alias="RABBIT_ROUTER_QUEUE_TITLE"
    )
    email_queue_title: str = Field(
        "email_queue", validation_alias="RABBIT_EMAIL_QUEUE_TITLE"
    )
    push_queue_title: str = Field(
        "push_queue", validation_alias="RABBIT_PUSH_QUEUE_TITLE"
    )

    @property
    def connection_url(self) -> str:
        """
        Формирует URL для подключения к RabbitMQ
        """
        return f"amqp://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/"


class DatabaseSettings(ModelConfig):
    """
    Настройки для базы данных
    database: Имя базы данных (по умолчанию notification)
    user: Пользователь базы данных (по умолчанию user)
    password: Пароль базы данных (по умолчанию password)
    host: Хост базы данных (по умолчанию 127.0.0.1)
    port: Порт базы данных (по умолчанию 5432)
    echo: Флаг для включения режима отладки (по умолчанию False)
    """

    database: str = Field("notification", validation_alias="POSTGRES_DB")
    user: str = Field("user", validation_alias="POSTGRES_USER")
    password: SecretStr = Field("password", validation_alias="POSTGRES_PASSWORD")
    host: str = Field("127.0.0.1", validation_alias="SQL_HOST")
    port: str = Field("5432", validation_alias="SQL_PORT")
    echo: bool = Field(False, validation_alias="DB_ECHO")

    @property
    def connection_url(self) -> str:
        """
        Формирует URL для подключения к базе данных
        """
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"

    @property
    def alembic_url(self) -> str:
        """Собирает URL для Alembic"""
        return f"postgresql+psycopg2://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class AdminSettings(ModelConfig):
    """
    Настройки для админ панели
    email: Email админ панели (по умолчанию admin@admin.com)
    password: Пароль админ панели (по умолчанию admin)
    token: Токен админ панели (по умолчанию admin)
    """

    email: str = Field("admin@admin.com", validation_alias="ADMIN_EMAIL")
    password: str = Field("admin", validation_alias="ADMIN_PASSWORD")
    token: str = Field("admin", validation_alias="ADMIN_TOKEN")
    secret_key: str = Field("secret_key", validation_alias="ADMIN_SECRET_KEY")


class EmailSettings(ModelConfig):
    """
    Настройки для сервиса email
    """

    from_address: str = Field("test@mail.ru", validation_alias="EMAIL_FROM_ADDRESS")
    smtp_host: str = Field("smtp.mail.ru", validation_alias="EMAIL_SMTP_HOST")
    smtp_port: int = Field(587, validation_alias="EMAIL_SMTP_PORT")
    smtp_user: str = Field("test@mail.ru", validation_alias="EMAIL_SMTP_USER")
    smtp_password: str = Field("password", validation_alias="EMAIL_SMTP_PASSWORD")


class Settings(BaseSettings):
    proect: ProjectSettings = ProjectSettings()
    auth: AuthSettings = AuthSettings()
    rabbit: RabbitSettings = RabbitSettings()
    db: DatabaseSettings = DatabaseSettings()
    admin: AdminSettings = AdminSettings()
    email: EmailSettings = EmailSettings()


settings = Settings()
