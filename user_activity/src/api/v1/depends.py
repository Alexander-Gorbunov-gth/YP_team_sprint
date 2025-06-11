import logging
import uuid
from typing import Annotated

from circuitbreaker import CircuitBreakerError, circuit
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from httpx import AsyncClient, RequestError
from pydantic import BaseModel
from src.core.config import settings
from src.infrastructure.clients.http import get_httpx_client
from src.services.bookmark import AbstractBookmarkService, get_bookmark_service
from src.services.like import AbstractLikeService, get_like_service
from src.services.review import AbstractReviewService, get_review_service

logger = logging.getLogger(__name__)

bookmark_serviceDep = Annotated[AbstractBookmarkService, Depends(get_bookmark_service)]
like_serviceDep = Annotated[AbstractLikeService, Depends(get_like_service)]
review_serviceDep = Annotated[AbstractReviewService, Depends(get_review_service)]

oauth2_scheme = HTTPBearer()


class User(BaseModel):
    sub: uuid.UUID
    role: list[str]


async def get_test_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    print(token.credentials)
    user = User(sub=uuid.UUID("3fa85f67-5717-4562-b3fc-2c963f66afa6"), role=["admin"])
    return user


@circuit(failure_threshold=5, recovery_timeout=15)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], httpx_client: Annotated[AsyncClient, Depends(get_httpx_client)]
) -> User:
    """Получение текущего пользователя из сервиса аутентификации"""

    try:
        response = await httpx_client.get(
            settings.auth.service_url, headers={"Authorization": f"Bearer {token.credentials}"}
        )
        if response.status_code == 401:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время жизни сессии истекло.")
        if response.status_code == 200:
            return User(**response.json())
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
    except CircuitBreakerError as e:
        logger.warning(f"Circuit Breaker: сервис аутентификации временно не доступен.")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
    except RequestError as e:
        logger.exception(f"Ошибка при получении текущего пользователя: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
    except Exception as e:
        logger.exception(f"Неизвестная ошибка при получении текущего пользователя: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
