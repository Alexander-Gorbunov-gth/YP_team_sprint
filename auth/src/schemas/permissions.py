from pydantic import BaseModel


class PermissionCreate(BaseModel):
    slug: str
    title: str
    description: str | None = None


class PermissionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class PermissionPublic(PermissionCreate):
    pass
