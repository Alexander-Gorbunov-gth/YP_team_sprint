from logging import config as logging_config
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


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
    """

    host: str = Field("localhost", validation_alias="RABBIT_HOST")
    port: int = Field(5672, validation_alias="RABBIT_PORT")
    user: str = Field("user", validation_alias="RABBIT_USER")
    password: SecretStr = Field("password", validation_alias="RABBIT_PASSWORD")
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
    def rabbit_url(self) -> str:
        """
        Формирует URL для подключения к RabbitMQ
        """
        return f"amqp://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/"


class DBSettings(ModelConfig):
    """
    Настройки базы данных.

    Attributes:
        db_type (str): Тип базы данных (по умолчанию 'postgres').
        db_name (str): Название базы данных (по умолчанию 'notifications_db').
        db_user (str): Имя пользователя базы данных (по умолчанию 'auth_user').
        db_password (SecretStr): Пароль пользователя базы данных (читается из переменной `DB_PASSWORD`).
        db_host (str): Хост базы данных (по умолчанию '127.0.0.1').
        db_port (int): Порт базы данных (по умолчанию 5432).
        db_echo (bool): Флаг включения SQL логов (по умолчанию True).
    """

    db_type: str = Field(default="postgres", validation_alias="DB_TYPE")
    db_name: str = Field(default="notifications_db", validation_alias="POSTGRES_DB")
    db_user: str = Field(default="auth_user", validation_alias="POSTGRES_USER")
    db_password: SecretStr = Field(..., validation_alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="127.0.0.1", validation_alias="SQL_HOST")
    db_port: int = Field(default=5432, validation_alias="SQL_PORT")
    db_echo: bool = Field(default=True, validation_alias="DB_ECHO")

    @property
    def db_url(self) -> str:
        """
        Генерирует URL для подключения к базе данных.

        Returns:
            str: URL для подключения.
        """
        return (
            f"{self.db_type}://{self.db_user}:"
            f"{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/"
            f"{self.db_name}"
        )


class Settings(BaseSettings):
    proect: ProjectSettings = ProjectSettings()
    auth: AuthSettings = AuthSettings()
    rabbit: RabbitSettings = RabbitSettings()
    db: DBSettings = DBSettings()


settings = Settings()
