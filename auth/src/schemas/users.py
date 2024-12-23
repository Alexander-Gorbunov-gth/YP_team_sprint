from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class RefreshToken(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class TokenResponse(AccessToken):
    token_type: str = Field(default="Bearer")


class TokenUserData(BaseModel):
    sub: str
    scope: list[str] = Field(default=[])
    iat: datetime
    access_exp: datetime
    refresh_exp: datetime
    jti: str


class LoginData(BaseModel):
    email: EmailStr
    password: str
