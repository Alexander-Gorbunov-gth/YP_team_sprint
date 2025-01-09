from pathlib import Path
from dotenv import find_dotenv

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class ModelConfig(BaseSettings):
    """
    Базовый класс конфигурации для всех настроек.

    Attributes:
        model_config (SettingsConfigDict): Указывает настройки для работы
        с .env файлом и игнорирование дополнительных параметров.
    """

    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.test"),  # Указывает путь к .env файлу
        env_file_encoding="utf-8",  # Кодировка .env файла
        extra="ignore",  # Игнорировать параметры, не описанные в модели
    )


class ServiceSettings(ModelConfig):
    """Настройки сервиса."""

    def get_api_v1(self):
        return f"{self.get_url()}/api/v1"


class DBSettings(ModelConfig):
    """
    Настройки базы данных.

    Attributes:
        db_type (str): Тип базы данных (по умолчанию 'postgres').
        db_name (str): Название базы данных (по умолчанию 'auth_db').
        db_user (str): Имя пользователя базы данных (по умолчанию 'auth_user').
        db_password (SecretStr): Пароль пользователя базы данных (читается из переменной `DB_PASSWORD`).
        db_host (str): Хост базы данных (по умолчанию '127.0.0.1').
        db_port (int): Порт базы данных (по умолчанию 5432).
        db_echo (bool): Флаг включения SQL логов (по умолчанию True).
    """

    postgres_type: str = Field(default="postgres", validation_alias="POSTGRES_TYPE")
    postgres_name: str = Field(default="auth_db", validation_alias="POSTGRES_DB")
    postgres_user: str = Field(default="auth_user", validation_alias="POSTGRES_USER")
    postgres_password: SecretStr = Field(..., validation_alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="127.0.0.1", validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    postgres_echo: bool = Field(default=False, validation_alias="POSTGRES_ECHO")

    @property
    def db_url(self) -> str:
        """
        Генерирует URL для подключения к базе данных.

        Returns:
            str: URL для подключения.
        """
        return (
            f"{self.postgres_type}://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_name}"
        )


class RedisSettings(ModelConfig):
    """
    Настройки Redis.

    Attributes:
        redis_host (str): Хост Redis (читается из переменной `REDIS_HOST`).
        redis_port (str): Порт Redis (читается из переменной `REDIS_PORT`).
    """

    redis_host: str = Field(default="127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: str = Field(..., validation_alias="REDIS_PORT")


class TestSettings(BaseSettings):
    """
    Основные настройки приложения.

    Attributes:
        service (ServiceSettings): Настройки сервиса.
        postgres (DBSettings): Настройки базы данных.
        redis (RedisSettings): Настройки Redis.
    """

    service: ServiceSettings = ServiceSettings()
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()


test_settings: TestSettings = TestSettings()
