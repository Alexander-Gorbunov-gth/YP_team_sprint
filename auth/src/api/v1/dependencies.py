from functools import wraps
from typing import Annotated

from fastapi import Depends, Request, Response, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import settings
from src.domain.entities import Token, User
from src.domain.exceptions import Forbidden, NotAuthorized
from src.domain.interfaces import AbstractAuthService, AbstractJWTService, AbstractSessionService
from src.domain.repositories import AbstractUserRepository, AbstractRoleRepository
from src.infrastructure.repositories.user import get_user_repository
from src.services.auth import get_auth_service
from src.services.jwt import get_jwt_service
from src.services.sessions import get_session_service
from src.services.role import get_role_service

SessionDep = Annotated[AbstractSessionService, Depends(get_session_service)]
AuthDep = Annotated[AbstractAuthService, Depends(get_auth_service)]
JWTDep = Annotated[AbstractJWTService, Depends(get_jwt_service)]
UserRepoDep = Annotated[AbstractUserRepository, Depends(get_user_repository)]
RoleServ = Annotated[AbstractRoleRepository, Depends(get_role_service)]

security = HTTPBearer()


def set_refresh_token(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.service.debug,
        samesite="Strict",
        max_age=settings.service.refresh_token_expire,
    )


def get_refresh_token(request: Request) -> str | None:
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise NotAuthorized
    return


def get_refresh_token_data(jwt_service: JWTDep, refresh_token: str = Depends(get_refresh_token)) -> Token:
    return jwt_service.decode_token(refresh_token)


async def get_current_user(user_repository: UserRepoDep, payload: Token = Depends(get_refresh_token_data)) -> User:
    user: User = await user_repository.get_by_id(payload.user_uuid)
    return user


def has_permission(required_permissions: list[str] | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(
            *args,
            request: Request,
            credentials: HTTPAuthorizationCredentials = Security(security),
            jwt_service: JWTDep,
            **kwargs,
        ):
            access_token = credentials.credentials
            payload = jwt_service.decode_token(jwt_token=access_token)
            if required_permissions is not None:
                if not set(required_permissions).issubset(set(payload.scope)):
                    raise Forbidden

            request.state.user = payload
            return func(*args, request=request, **kwargs)

        return wrapper

    return decorator
