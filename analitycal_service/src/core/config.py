from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    project_name: str = Field(default="Analytical service", validation_alias="PROJECT_NAME")
    debug: bool = Field(default=True, validation_alias="DEBUG")


class BrockerSettings(ModelConfig):
    topic_name: str = Field(default="event_topic", validation_alias="TOPIC_NAME")
    bootstrap_service: str = Field(..., validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_username: str = Field(..., validation_alias="KAFKA_USERNAME")
    kafka_password: str = Field(..., validation_alias="KAFKA_PASSWORD")


class Settings(BaseSettings):
    brocker: BrockerSettings = BrockerSettings()
    service: ServiceSettings = ServiceSettings()


settings = Settings()
