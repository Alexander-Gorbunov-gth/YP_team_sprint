from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class PermissionBase(BaseModel):
    slug: str
    description: str | None


class PermissionResponse(PermissionBase):
    pass


class PermissionCreate(PermissionBase):
    pass
