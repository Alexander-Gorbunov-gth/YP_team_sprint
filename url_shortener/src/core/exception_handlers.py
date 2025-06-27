from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Any, NoReturn

from fastapi import HTTPException, Request, Response

from src.domain.exceptions import (
    ShortUrlNotFound
)


def create_exception_handler(
    status_code: int, detail: str
) -> Callable[[Request, Exception], Coroutine[Any, Any, NoReturn]]:
    """
    Фабрика для создания обработчиков исключений.

    :param status_code: HTTP-статус, который будет возвращён.
    :param detail: Сообщение об ошибке для клиента.
    :return: Функция-обработчик исключения.
    """

    async def handler(request: Request, exc: Exception) -> NoReturn:
        raise HTTPException(status_code=status_code, detail=detail)

    return handler


short_url_not_found_handler = create_exception_handler(
    status_code=HTTPStatus.NOT_FOUND,
    detail="Ссылка не найдена.",
)


exception_handlers: dict[
    type[Exception],
    Callable[[Request, Exception], Coroutine[Any, Any, Response]],
] = {
    ShortUrlNotFound: short_url_not_found_handler
}
