from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow")

    # Bench
    col_requests: int

    # MongoDB
    mongodb_host: str
    mongodb_port: int
    mongodb_db: str

    # PostgreSQL
    postgres_host: str
    postgres_port: int
    postgres_username: str
    postgres_password: str
    postgres_db: str

    # @property
    # def clickhouse_dict(self):
    #     return {
    #         "host": self.clickhouse_host,
    #         "port": self.clickhouse_port,
    #         "username": self.clickhouse_username,
    #         "password": self.clickhouse_password
    #     }

    # @property
    # def vertica_dict(self):
    #     return {
    #         "host": self.vertica_host,
    #         "port": self.vertica_port,
    #         "user": self.vertica_username,
    #         "password": self.vertica_password
    #     }


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
