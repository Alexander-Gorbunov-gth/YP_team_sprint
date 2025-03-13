from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    id: UUID | None
    email: str
    password: str
    is_active: bool


@dataclass
class Token:
    user_uuid: str
    iat: str
    exp: str
    jti: str
    scope: list[str]


@dataclass
class Permission:
    slug: str
    description: str


@dataclass
class Role:
    slug: str
    title: str
    description: str
    permissions: list[Permission]
