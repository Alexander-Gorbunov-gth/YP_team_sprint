from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv()


class Settings(BaseSettings):
    project_name: str = 'movies'
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    elastic_host: str = '127.0.0.1'
    elastic_port: int = 9200

    @property
    def elastic_url(self) -> str:
        """Формируем URL для подключения к Elasticsearch."""
        return f'http://{self.elastic_host}:{self.elastic_port}'

    @property
    def redis_url(self) -> str:
        """Формируем URL для подключения к Redis"""
        return f'http://{self.redis_host}:{self.redis_port}'

    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "allow"


settings = Settings()
