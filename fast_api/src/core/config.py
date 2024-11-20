from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'movies'
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    ELASTIC_HOST: str = '127.0.0.1'
    ELASTIC_PORT: int = 9200
    REDIS_PASSWORD: str

    @property
    def elastic_url(self) -> str:
        """Формируем URL для подключения к Elasticsearch."""
        return f'http://{self.ELASTIC_HOST}:{self.ELASTIC_PORT}'

    @property
    def redis_url(self) -> str:
        """Формируем URL для подключения к Redis"""
        return f'http://{self.REDIS_HOST}:{self.REDIS_PORT}'

    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "allow"


settings = Settings()
