from typing import Annotated
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterForm(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserResponse(BaseModel):
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginForm(BaseModel):
    email: Annotated[EmailStr, Form(...)]
    password: Annotated[str, Form(...)]


class LoginResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str = Field(default="jwt")


class UserIdResponse(BaseModel):
    id: UUID
    username: str


class DjangoLoginResponse(BaseModel):
    id: UUID
    email: str
    roles: list[str]
    is_active: bool
