from uuid import UUID
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: UUID | None
    email: str
    password: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Token:
    user_uuid: str
    iat: str
    exp: str
    jti: str
    scope: list[str]


@dataclass
class Session:
    id: UUID | None
    user_id: UUID
    user_agent: str
    jti: UUID
    refresh_token: str
    user_ip: str | None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
