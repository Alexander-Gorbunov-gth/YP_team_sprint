from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    topic_name: str = Field(default="event_topic", validation_alias="TOPIC_NAME")
    bootstrap_service: str = Field(..., validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_username: str = Field(..., validation_alias="KAFKA_USERNAME")
    kafka_password: str = Field(..., validation_alias="KAFKA_PASSWORD")

    def get_init_conf(self) -> dict:
        return {
            "bootstrap_servers": self.bootstrap_service,
            "security_protocol": "SASL_PLAINTEXT",
            "sasl_mechanism": "PLAIN",
            "sasl_plain_username": self.kafka_username,
            "sasl_plain_password": self.kafka_password,
            "enable_auto_commit": False,
        }

class ClickHouseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CH_")
    host: str = Field(..., alias="CLICKHOUSE_HOST")
    port: int = Field(..., alias="CLICKHOUSE_PORT")
    user: str = Field(..., alias="CLICKHOUSE_USER")
    password: str = Field(..., alias="CLICKHOUSE_PASSWORD")
    database: str = Field(..., alias="CLICKHOUSE_DATABASE")
    secure: bool = Field(..., alias="CLICKHOUSE_USESSL")

    def get_init_conf(self) -> dict:
        return self.model_dump()


class Settings(BaseSettings):
    debug: bool = Field(..., alias="DEBUG")
    batch_size: int = Field(..., alias="BATCH_SIZE_KAFKA_CLICKHOUSE")
    kafka_settings: KafkaSettings = KafkaSettings()
    clickhouse_settings: ClickHouseSettings = ClickHouseSettings()


settings = Settings()
