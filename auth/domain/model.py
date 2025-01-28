from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class DeviceType(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    OTHER = "other"


class IDMixin(BaseModel):
    id: UUID | None = Field(default=None, description="ID сущности.")


class Permission(IDMixin):
    name: str = Field(..., max_length=155, description="Наименование права.")
    description: str | None = Field(default=None, description="Описание права.")


class Role(IDMixin):
    name: str = Field(..., max_length=155, description="Наименование роли.")
    description: str | None = Field(default=None, description="Описание роли.")
    permissions: list = Field(default_factory=list, description="Права роли.")


class User(IDMixin):
    email: EmailStr = Field(..., description="")
    hashed_password: str = Field(..., description="")
    is_active: bool = Field(default=False, description="")
    roles: list[Role] = Field(default_factory=list, description="")
    sessions: list["Session"] = Field(default_factory=list, description="")

    def has_permission(self, permission_name: str) -> bool:
        for role in self.roles:
            if any(permission.name == permission_name for permission in role.permissions):
                return True
        return False



class Session(IDMixin):
    user_id: UUID = Field(..., description="")
    type_device: DeviceType = Field(..., description="")
    ip_address: str | None = Field(default=None, description="IP-адрес пользователя")
    location: str | None = Field(None, description="Геолокация пользователя")
    access_token: str | None = Field(default=None, description="Текущий access-токен")
    refresh_token: str | None = Field(default=None, description="Текущий refresh-токен")
    is_active: bool = Field(default=True, description="Активна ли сессия")
