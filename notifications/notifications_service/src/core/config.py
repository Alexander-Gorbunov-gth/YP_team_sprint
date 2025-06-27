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


class Settings(BaseSettings):
    proect: ProjectSettings = ProjectSettings()
    auth: AuthSettings = AuthSettings()
    rabbit: RabbitSettings = RabbitSettings()


settings = Settings()
