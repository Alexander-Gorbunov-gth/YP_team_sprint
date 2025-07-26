from dishka import FromDishka
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.entities.user import User
from src.services.exceptions import SessionHasExpired
from src.services.jwt import AbstractJWTService

auth_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    jwt_service: FromDishka[AbstractJWTService], credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> User:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо авторизоваться")

    token = credentials.credentials
    try:
        user = jwt_service.decode_token(token)
        return user
    except SessionHasExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Сессия истекла")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")
