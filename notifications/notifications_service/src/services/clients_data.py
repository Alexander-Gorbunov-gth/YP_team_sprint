import logging
from fastapi import Depends, HTTPException, status
from pydantic import parse_obj_as
from typing import AsyncGenerator, Generator, List
from circuitbreaker import CircuitBreakerError, circuit
from httpx import AsyncClient, RequestError

from src.infrastructure.clients import AbstractDataClientsService
from src.domain.clients import Client
from src.domain.tasks import TaskMessage


from src.core.config import settings
from src.infrastructure.connections.http import httpx_client

logger = logging.getLogger(__name__)

class HttpxClientsDataService(AbstractDataClientsService):

    @circuit(failure_threshold=5, recovery_timeout=15)
    async def fetch_clients_data(self, uuids: list[str] | None = None, page_number: int | None = None) -> list[Client]:
        """Получает список данных польщователей пачками по страницам page_number"""
        if not uuids:
            uuids = []
        try:
            params = {"page_number": page_number, "uuids": ",".join(uuids)}
            response = await httpx_client.get(
                settings.auth.service_url, headers={"Authorization": f"Bearer {settings.auth.token}"}, params=params
            )
            if response.status_code == 401:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время жизни сессии истекло.")
            if response.status_code == 200:
                result = response.json()
                return parse_obj_as(List[Client], result.get("clients", []))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
        except CircuitBreakerError as e:
            logger.warning(f"Circuit Breaker: сервис аутентификации временно не доступен.")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
        except RequestError as e:
            logger.exception(f"Ошибка при получении текущего пользователя: {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении данных пользователей: {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис временно не доступен.")
    
    async def get_clients_data(self, uuids: list[str] | None = None, for_all_users: bool = False) -> AsyncGenerator[list[Client], None]:
        page_number = 0
        if not for_all_users and not uuids:
            return []
        while True:
            batch_clients_data = await self.fetch_clients_data(uuids, page_number)
            if not batch_clients_data:
                break
            yield batch_clients_data
            page_number += 1

    

def get_clients_data_service() -> HttpxClientsDataService:
    return HttpxClientsDataService()
