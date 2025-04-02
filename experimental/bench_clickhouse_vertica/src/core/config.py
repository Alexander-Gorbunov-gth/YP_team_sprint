from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow")

    # Bench
    col_requests: int

    # ClickHouse
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_username: str
    clickhouse_password: str

    # Vertica
    vertica_host: str
    vertica_port: int
    vertica_username: str
    vertica_password: str

    @property
    def clickhouse_dict(self):
        return {
            "host": self.clickhouse_host,
            "port": self.clickhouse_port,
            "username": self.clickhouse_username,
            "password": self.clickhouse_password
        }

    @property
    def vertica_dict(self):
        return {
            "host": self.vertica_host,
            "port": self.vertica_port,
            "user": self.vertica_username,
            "password": self.vertica_password
        }


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
