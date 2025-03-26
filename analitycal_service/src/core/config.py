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


class ProducerSettings(ModelConfig):
    topic_name: str = Field(default="event_topic", validation_alias="TOPIC_NAME")
    bootstrap_service: str = Field(..., validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_username: str = Field(..., validation_alias="KAFKA_USERNAME")
    kafka_password: str = Field(..., validation_alias="KAFKA_PASSWORD")


class Settings(BaseSettings):
    producer: ProducerSettings = ProducerSettings()


settings = Settings()
