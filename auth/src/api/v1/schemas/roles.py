from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .permissions import PermissionResponse
from src.domain.entities import Permission


class RoleCreateOrUpdate(BaseModel):
    slug: str
    title: str
    description: str | None
    permissions: list[str] = Field(..., min_length=1)


class RoleResponse(BaseModel):
    slug: str
    title: str
    description: str | None
    permissions: list[PermissionResponse]


class AddOrDeleteRoleToUser(BaseModel):
    role_slug: str
    user_id: str
