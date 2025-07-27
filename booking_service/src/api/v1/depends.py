from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.entities.user import User
from src.services.exceptions import SessionHasExpired
from src.services.jwt import AbstractJWTService

auth_scheme = HTTPBearer(auto_error=False)


@inject
async def get_current_user(
    jwt_service: FromDishka[AbstractJWTService], credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> User:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо авторизоваться")

    token = credentials.credentials
    try:
        user = jwt_service.decode_token(token)
        return user
    except SessionHasExpired as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Сессия истекла") from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен") from e


CurrentUserDep = Annotated[User, Depends(get_current_user)]
