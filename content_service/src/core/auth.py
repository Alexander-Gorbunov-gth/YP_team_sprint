import http
from logging import getLogger
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from src.core.config import settings

logger = getLogger(__name__)


def decode_token(token: str) -> Optional[dict]:

    try:
        return jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_alg]
        )
    except Exception as e:
        logger.error(f"Error decode token: {e}")
        return None


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:

        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if not credentials:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail="Invalid authorization code.",
            )
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail="Only Bearer token might be accepted",
            )
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail="Invalid or expired token.",
            )
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> Optional[dict]:
        return decode_token(jwt_token)


security_jwt = JWTBearer()


def require_permissions(required_permissions: list[str] | None = None):
    """
    Фабрика зависимостей (dependencies),
    которая возвращает функцию проверки прав на основе access-токена.
    :param required_permissions: Список требуемых прав
    :return: Асинхронная функция check_permission
    """

    async def check_permission(
        request: Request,
        user: Annotated[dict, Depends(security_jwt)],
    ):
        logger.debug("Проверяем права доступа...")
        if required_permissions and not set(required_permissions).issubset(
            set(user["scope"])
        ):
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail="User dont have rules.",
            )
        return True

    return check_permission
