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
class Session:
    id: UUID | None
    user_id: UUID
    user_agent: str
    jti: UUID
    refresh_token: str
    user_ip: str | None
    is_active: bool
