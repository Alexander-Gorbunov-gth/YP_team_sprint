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
    decription: str = Field("", validation_alias="PROJECT_DESCRIPTION")
    debug: bool = Field(False, validation_alias="DEBUG")


class AuthSettings(ModelConfig):
    """
    Настройки для сервиса авторизации
    auth_service_url: Ссылка на сервис авторизации (по умолчанию None)
    auth_token: Токен для авторизации (по умолчанию None)
    """

    service_url: str | None = Field(None, validation_alias="AUTH_SERVICE_URL")
    token: str | None = Field(None, validation_alias="AUTH_TOKEN")



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


class Settings(BaseSettings):
    proect: ProjectSettings = ProjectSettings()
    auth: AuthSettings = AuthSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
