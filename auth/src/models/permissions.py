from sqlmodel import SQLModel, Field

from .mixins import DateTimeMixin


class BasePermission(SQLModel):
    title: str
    description: str | None


class Permission(BasePermission, DateTimeMixin, table=True):
    code: str = Field(default=None, primary_key=True)


class PermissionPublic(BasePermission):
    """Для ответов АПИ"""
    code: str


class PermissionCreate(BasePermission):
    """Для тела Post запроса"""
    code: str