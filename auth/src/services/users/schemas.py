from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=255)
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)


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

    class Config:
        orm_mode = True
