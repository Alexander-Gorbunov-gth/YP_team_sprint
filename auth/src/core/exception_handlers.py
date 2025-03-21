from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Any, NoReturn

from fastapi import HTTPException, Request, Response
from src.domain.exceptions import (
    Forbidden,
    PasswordsNotMatch,
    SessionHasExpired,
    UserIsExists,
    UserNotFound,
    WrongEmailOrPassword,
    WrongOldPassword,
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


user_exists_handler = create_exception_handler(
    status_code=HTTPStatus.BAD_REQUEST,
    detail="Пользователь с таким email уже существует.",
)

passwords_not_match_handler = create_exception_handler(
    status_code=HTTPStatus.BAD_REQUEST, detail="Пароли не совпадают"
)

forbidden_handler = create_exception_handler(
    status_code=HTTPStatus.FORBIDDEN, detail="Доступ запрещен."
)

not_authorized_handler = create_exception_handler(
    status_code=HTTPStatus.UNAUTHORIZED, detail="Время жизни сессии истекло."
)

user_not_found_handler = create_exception_handler(
    status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден"
)

wrong_email_or_password = create_exception_handler(
    status_code=HTTPStatus.UNAUTHORIZED, detail="Неверный email или пароль"
)

wrong_old_password = create_exception_handler(
    status_code=HTTPStatus.BAD_REQUEST, detail="Неправильный текущий пароль"
)


exception_handlers: dict[
    type[Exception],
    Callable[[Request, Exception], Coroutine[Any, Any, Response]],
] = {
    UserIsExists: user_exists_handler,
    PasswordsNotMatch: passwords_not_match_handler,
    Forbidden: forbidden_handler,
    SessionHasExpired: not_authorized_handler,
    UserNotFound: user_not_found_handler,
    WrongEmailOrPassword: wrong_email_or_password,
    WrongOldPassword: wrong_old_password,
}
