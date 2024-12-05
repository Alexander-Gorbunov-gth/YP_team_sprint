from sqlmodel import SQLModel, Field

from .mixins import DateTimeMixin


class UserBase(SQLModel):
    """Базовая модель"""
    username: str = Field(unique=True)
    is_superuser: bool = False
    disabled: bool = False


class User(UserBase, table=True):
    """Для БД"""
    uuid: str | None = Field(default=None, primary_key=True)
    password: str

    def __str__(self) -> str:
        return f"User - {self.username}"


class UserPublic(UserBase):
    """Модель для ответа эндпоинта"""
    pass


class UserLogin(SQLModel):
    """Модель для POST запроса login"""
    username: str
    password: str


class Token(SQLModel):
    """Модель ответа для эндпоинт токена"""
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(SQLModel):
    """Модель для payload токена"""
    uuid: str | None = None
