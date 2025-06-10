from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ProjectSettings(ModelConfig):
    """
    Настройки для проекта
    title: Название проекта (по умолчанию User activity service)
    decription: Описание проекта (по умолчанию "")
    debug: Флаг для включения режима отладки (по умолчанию False)
    """

    title: str = Field("User activity service", validation_alias="PROJECT_TITLE")
    decription: str = Field("", validation_alias="PROJECT_DESCRIPTION")
    debug: bool = Field(False, validation_alias="DEBUG")


class MongoSettings(ModelConfig):
    """
    Настройки для MongoDB
    host: Хост MongoDB (по умолчанию 127.0.0.1)
    port: Порт MongoDB (по умолчанию 27017)
    username: Имя пользователя MongoDB (по умолчанию None)
    password: Пароль MongoDB (по умолчанию None)
    db_name: Имя базы данных MongoDB (по умолчанию None)
    """

    host: str = Field("127.0.0.1", validation_alias="MONGO_HOST")
    port: int = Field(27017, validation_alias="MONGO_PORT")
    username: str | None = Field(None, validation_alias="MONGO_USERNAME")
    password: SecretStr | None = Field(None, validation_alias="MONGO_PASSWORD")
    db_name: str = Field(..., validation_alias="MONGO_DB_NAME")

    @property
    def connection_url(self):
        if self.username and self.password:
            pwd = self.password.get_secret_value()
            return f"mongodb://{self.username}:{pwd}@{self.host}:{self.port}"
        return f"mongodb://{self.host}:{self.port}"


class AuthSettings(ModelConfig):
    """
    Настройки для сервиса авторизации
    auth_service_url: Ссылка на сервис авторизации (по умолчанию None)
    auth_token: Токен для авторизации (по умолчанию None)
    """

    service_url: str | None = Field(None, validation_alias="AUTH_SERVICE_URL")
    token: str | None = Field(None, validation_alias="AUTH_TOKEN")


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    proect: ProjectSettings = ProjectSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
