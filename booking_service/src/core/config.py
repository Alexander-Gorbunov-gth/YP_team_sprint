from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env",), extra="ignore")


class PostgresSettings(ModelConfig):
    """Настройки Postgres"""

    host: str = Field(default="127.0.0.1", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    db_name: str = Field(default="postgres", validation_alias="POSTGRES_DB_NAME")
    user: str = Field(default="postgres", validation_alias="POSTGRES_USER")
    password: SecretStr = Field(..., validation_alias="POSTGRES_PASSWORD")
    echo: bool = Field(default=False, validation_alias="POSTGRES_ECHO")

    @property
    def connection_url(self) -> str:
        """Ссылка для подключения с драйвером asyncpg"""

        pwd = self.password.get_secret_value()
        return f"postgresql+asyncpg://{self.user}:{pwd}@{self.host}:{self.port}/{self.db_name}"

    @property
    def alembic_url(self) -> str:
        """Ссылка для подключения с драйвером psypsycopg2"""

        pwd = self.password.get_secret_value()
        return f"postgresql+psypsycopg2://{self.user}:{pwd}@{self.host}:{self.port}/{self.db_name}"


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
