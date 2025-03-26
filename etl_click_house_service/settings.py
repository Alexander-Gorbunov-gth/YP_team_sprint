from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# class KafkaSettings(BaseSettings):
#     model_config = SettingsConfigDict(env_prefix="postgres_")
#     host: str = Field(..., alias="SQL_HOST")
#     port: int = Field(..., alias="SQL_PORT")
#     dbname: str = Field(..., alias="POSTGRES_DB")
#     user: str = ...
#     password: str = ...


class ClickHouseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CH_")
    host: str = Field(..., alias="CLICKHOUSE_HOST")
    port: str = Field(..., alias="CLICKHOUSE_PORT")
    user: str = Field(..., alias="CLICKHOUSE_USER")
    password: str = Field(..., alias="CLICKHOUSE_PASSWORD")
    database: str = Field(..., alias="CLICKHOUSE_DATABASE")
    secure: bool = Field(..., alias="CLICKHOUSE_USESSL")

    def get_data(self) -> dict:
        # return self.model_dump()
        return {
            "host": "ofsok90ydh.germanywestcentral.azure.clickhouse.cloud",
            "port": "8443",
            "user": "default",
            "password": "cjh72mrPIGd.f",
            "database": "__default__",
            "secure": True
        }


class Settings(BaseSettings):
    debug: bool = Field(..., alias="DEBUG")
    # database_settings: DatabaseSettings = DatabaseSettings()
    clickhouse_settings: ClickHouseSettings = ClickHouseSettings()


settings = Settings()
