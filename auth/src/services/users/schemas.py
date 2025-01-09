from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=255)
    full_name: str | None = Field(None, max_length=255)
    role_id: UUID | None = Field(None)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

    @field_validator("password")
    def validate_password(cls, password):
        if not any(char.isupper() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(char.islower() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not any(char.isdigit() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return password


class UserUpdate(UserCreate):
    pass


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserBase):
    pass


class RoleEnum(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    EDITOR = "Editor"
    VIEWER = "Viewer"
    MODERATOR = "Moderator"
    DEVELOPER = "Developer"
    SUPPORT = "Support"
    GUEST = "Guest"
    AUDITOR = "Auditor"
    CONTRIBUTOR = "Contributor"


class UserRole(BaseModel):
    id: UUID
    title: RoleEnum
