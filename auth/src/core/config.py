from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from dotenv import load_dotenv

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # project_name: str = Field('movies', validation_alias='PROJECT_NAME')


    # redis_host: str = Field('127.0.0.1', validation_alias='REDIS_HOST')
    # redis_port: int = Field(6379, validation_alias='REDIS_PORT')
    # redis_password: SecretStr | None = Field(None, validation_alias='REDIS_PASSWORD')

    model_config = SettingsConfigDict(
        env_file='.auth.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    debug: bool
    redis_url: str = "redis://localhost:6379"
    db_url: str
    secret_key_jwt: str

    # @property
    # def redis_url(self) -> str:
    #     """Формируем URL для подключения к Redis"""
    #     return f'http://{self.redis_host}:{self.redis_port}'


settings = Settings()
