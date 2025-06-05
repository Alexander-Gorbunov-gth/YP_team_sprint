from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ProjectSettings(ModelConfig):
    title: str = Field("User activity service", validation_alias="PROJECT_TITLE")
    decription: str = Field("", validation_alias="PROJECT_DESCRIPTION")
    debug: bool = Field(False, validation_alias="DEBUG")


class MongoSettings(ModelConfig):
    host: str = Field("127.0.0.1", validation_alias="MONGO_HOST")
    port: int = Field(27017, validation_alias="MONGO_PORT")
    username: str | None = Field(None, validation_alias="MONGO_USERNAME")
    password: SecretStr | None = Field(None, validation_alias="MONGO_PASSWORD")
    db_name: str = Field(..., validation_alias="MONGO_DB_NAME")

    @property
    def connection_url(self):
        if self.username and self.password:
            pwd = self.password.get_secret_value()
            return f"mongodb://{self.username}:{pwd}@{self.host}:{self.host}"
        return f"mongodb://{self.host}:{self.port}"


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    proect: ProjectSettings = ProjectSettings()


settings = Settings()
