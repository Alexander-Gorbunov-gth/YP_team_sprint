from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from .permissions import PermissionResponse


class RoleCreateOrUpdate(BaseModel):
    slug: str
    title: str
    description: str | None
    permissions: list[str]


class RoleResponse(BaseModel):
    slug: str
    title: str
    description: str | None
    permissions: list[PermissionResponse]


class PermissionCreate(RoleBase):
    pass


    permissions: list[Permission]