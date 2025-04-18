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
    producer_topic_name: str = Field(default="event_topic", validation_alias="PRODUCER_TOPIC")

    auth_topic_name: str = Field(default="auth_topic", validation_alias="CONSUMER_TOPICS")
    consumer_group_id: str = Field(default="analytic_services", validation_alias="CONSUMER_GROUP_ID")
    auth_topic_key: str = Field(default="analytic_service", validation_alias="AUTH_TOPIC_KEY")

    bootstrap_service: str = Field(..., validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_username: str = Field(..., validation_alias="KAFKA_USERNAME")
    kafka_password: str = Field(..., validation_alias="KAFKA_PASSWORD")

    @property
    def consumer_topics(self) -> list[str]:
        topics = []
        topics.append(self.auth_topic_name)
        return topics


class RedisSettings(ModelConfig):
    redis_host: str = Field(default="127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")
    redis_username: str | None = Field(default=None, validation_alias="REDIS_USERNAME")
    redis_password: str | None = Field(default=None, validation_alias="REDIS_PASSWORD")

    @property
    def redis_url(self) -> str:
        if self.redis_username is not None:
            if self.redis_password is not None:
                return f"redis://{self.redis_username}:{self.redis_password}@{self.redis_host}:{self.redis_port}"
            raise ValueError("Если указан был пользователь для Redis нужно указать и пароль.")
        return f"redis://{self.redis_host}:{self.redis_port}"


class Settings(BaseSettings):
    brocker: BrockerSettings = BrockerSettings()
    service: ServiceSettings = ServiceSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
