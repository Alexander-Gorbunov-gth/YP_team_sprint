from logging import config as logging_config
from pathlib import Path
from dotenv import find_dotenv

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ModelConfig(BaseSettings):
    """
    Базовый класс конфигурации для всех настроек.

    Attributes:
        model_config (SettingsConfigDict): Указывает настройки для работы с .env файлом и
        игнорирование дополнительных параметров.
    """

    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.dev"),  # Указывает путь к .env файлу
        env_file_encoding="utf-8",  # Кодировка .env файла
        extra="ignore",  # Игнорировать параметры, не описанные в модели
    )


class ServiceSettings(ModelConfig):
    """
    Настройки сервиса.

    Attributes:
        base_dir (Path): Базовый путь проекта.
        secret_key (SecretStr): Секретный ключ приложения (читается из переменной окружения `SECRET_KEY`).
        jwt_algorithm (str): Алгоритм для JWT токенов (читается из переменной окружения `JWT_ALGORITHM`).
        debug (bool): Флаг режима отладки (по умолчанию False, читается из переменной `DEBAG`).
    """

    base_dir: Path = Path(__file__).parent.parent.parent
    project_name: str = Field(default="auth service", validation_alias="PROJECT_NAME")
    secret_key: SecretStr = Field(..., validation_alias="SECRET_KEY")
    jwt_algorithm: str = Field(..., validation_alias="JWT_ALGORITHM")
    debug: bool = Field(default=False, validation_alias="DEBAG")
    refresh_token_expire: int = Field(
        default=6000, validation_alias="REFRESH_TOKEN_EXPIRE"
    )
    access_token_expire: int = Field(
        default=6000, validation_alias="ACCESS_TOKEN_EXPIRE"
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
        db_echo (bool): Флаг включения SQL логов (по умолчанию True).
    """

    db_type: str = Field(default="postgres", validation_alias="DB_TYPE")
    db_name: str = Field(default="auth_db", validation_alias="DB_NAME")
    db_user: str = Field(default="auth_user", validation_alias="DB_USER")
    db_password: SecretStr = Field(..., validation_alias="DB_PASSWORD")
    db_host: str = Field(default="127.0.0.1", validation_alias="DB_HOST")
    db_port: int = Field(default=5432, validation_alias="DB_PORT")
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


settings: Settings = Settings()
