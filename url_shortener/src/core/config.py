from logging import config as logging_config
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ModelConfig(BaseSettings):
    """
    Базовый класс конфигурации для всех настроек.
    model_config (SettingsConfigDict): Указывает настройки для работы с .env файлом и игнорирование дополнительных параметров.
    """

    model_config = SettingsConfigDict(
        env_file=(".env"),  # Указывает путь к .env файлу
        env_file_encoding="utf-8",  # Кодировка .env файла
        extra="ignore",  # Игнорировать параметры, не описанные в модели
    )


class ServiceSettings(ModelConfig):
    base_dir: Path = Path(__file__).parent.parent.parent
    project_name: str = Field(
        default="url shortener service", validation_alias="PROJECT_NAME"
    )
    debug: bool = Field(default=True, validation_alias="DEBUG")
    short_code_length: int = Field(
        default=8, validation_alias="SHORT_CODE_LENGTH"
    )
    expires_days: int = Field(
        default=365, validation_alias="EXPIRES_DAYS"
    )
    cron: str = Field(
        default="0 0 * * *", validation_alias="CRON"
    )
    domain: str = Field(
        default="http://127.0.0.1:8000/", validation_alias="DOMAIN"
    )


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
    """

    db_type: str = Field(default="postgresql+asyncpg", validation_alias="DB_TYPE")
    db_name: str = Field(default="url_shortener_db", validation_alias="POSTGRES_DB")
    db_user: str = Field(default="auth_user", validation_alias="POSTGRES_USER")
    db_password: SecretStr = Field(..., validation_alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="127.0.0.1", validation_alias="SQL_HOST")
    db_port: int = Field(default=5432, validation_alias="SQL_PORT")

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


class RedisSettings(ModelConfig):
    """
    Настройки Redis.

    Attributes:
        redis_host (str): Хост Redis (читается из переменной `REDIS_HOST`).
        redis_port (str): Порт Redis (читается из переменной `REDIS_PORT`).
    """

    redis_host: str = Field(..., validation_alias="REDIS_HOST")
    redis_port: str = Field(..., validation_alias="REDIS_PORT")

    @property
    def redis_url(self) -> str:
        """
        Генерирует URL для подключения к Redis.

        Returns:
            str: URL подключения к Redis.
        """
        return f"redis://{self.redis_host}:{self.redis_port}"


class Settings(BaseSettings):
    service: ServiceSettings = ServiceSettings()
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
