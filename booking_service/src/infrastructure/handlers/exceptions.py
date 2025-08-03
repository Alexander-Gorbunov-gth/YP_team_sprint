from collections.abc import Callable, Coroutine
from typing import Any, NoReturn
from fastapi import HTTPException, Request, Response, status

from src.services.exceptions import EventNotFoundError, EventNotOwnerError, EventStartDatetimeError, EventTimeConflictError

def create_exception_handler(status_code: int, detail: str) -> Callable[[Request, Any], Coroutine[Any, Any, Response]]:
    """
    Фабрика для создания исключений
    :param status_code: код статуса
    :param detail: текст ошибки
    :return: HTTPException
    """

    async def handler(request: Request, exc: Exception) -> NoReturn:
        raise HTTPException(status_code=status_code, detail=detail)
    return handler


exception_handlers: dict[type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]] = {
    EventNotFoundError: create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено."),
    EventNotOwnerError: create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для выполнения операции."),
    EventStartDatetimeError: create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректная дата начала события."),
    EventTimeConflictError: create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, detail="Время пересекается с другим событием."),
}