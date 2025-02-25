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


token = Token(user_uuid=123, iat=56, exp=2, jti=3421, scope=65)
print(token)
