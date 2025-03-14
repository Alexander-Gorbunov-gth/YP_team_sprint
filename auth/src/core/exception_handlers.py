from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Any, NoReturn

from fastapi import HTTPException, Request, Response

from src.domain.exceptions import Forbidden, NotAuthorized, PasswordsNotMatch, UserIsExists


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


user_exists_handler = create_exception_handler(
    status_code=HTTPStatus.BAD_REQUEST,
    detail="Пользователь с таким email уже существует.",
)

passwords_not_match_handler = create_exception_handler(status_code=HTTPStatus.BAD_REQUEST, detail="Пароли не совпадают")

forbidden_handler = create_exception_handler(status_code=HTTPStatus.FORBIDDEN, detail="Доступ запрещен.")

not_authorized_handler = create_exception_handler(
    status_code=HTTPStatus.UNAUTHORIZED, detail="Время жизни сессии истекло."
)


exception_handlers: dict[type[Exception], Callable[[Request, Exception], Coroutine[Any, Any, Response]]] = {
    UserIsExists: user_exists_handler,
    PasswordsNotMatch: passwords_not_match_handler,
    Forbidden: forbidden_handler,
    NotAuthorized: not_authorized_handler,
}
