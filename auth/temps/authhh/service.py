from functools import lru_cache
import uuid
from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends

from sqlalchemy.exc import IntegrityError
from src.schemas.users import Payload, TokenResponse, RefreshToken
from src.schemas.sessions import SessionCreate
from src.models.users import User
from src.services.authh.uow import get_auth_uow
from src.services.users.schemas import UserResponse, UserCreate
from src.services.authh.interfaces import IAuthService, IAuthUoW, IBlackList
from src.services.authh.black_list import get_black_list_service
from src.services.authh.exceptions import (
    UserIsExist,
    UserNotFoundError,
    InvalidPasswordError,
)
from src.services.authh.password import get_password_hash, verify_password
from src.services.authh.tokens import (
    TokenFactory,
    get_token_factory,
    REFRESH_EXPIRE_DAYS,
)


class AuthService(IAuthService):
    """
    Сервис для управления процессами аутентификации и авторизации.
    """

    def __init__(
        self, uow: IAuthUoW, token_factory: TokenFactory, black_list: IBlackList
    ) -> None:
        """
        Инициализация сервиса аутентификации.

        :param uow: Единица работы (Unit of Work) для управления транзакциями.
        :param token_factory: Фабрика токенов для создания JWT.
        """

        self._uow: IAuthUoW = uow
        self._token_factory = token_factory
        self._black_list = black_list

    async def register(self, user: UserCreate) -> User:
        """
        Регистрация нового пользователя.

        :param user: Данные для создания нового пользователя.
        :return: Сериализованные данные созданного пользователя.
        :raises UserIsExist: Если пользователь с таким email уже существует.
        """

        async with self._uow as uow:
            user.password = get_password_hash(user.password)
            try:
                user = await uow.users.add(user)
            except IntegrityError:
                raise UserIsExist
            return UserResponse(**await user.to_dict())

    async def login(
        self, email: str, password: str, headers: dict[str, Any]
    ) -> tuple[RefreshToken, TokenResponse]:
        """
        Вход пользователя в систему.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param headers: Заголовки запроса для получения информации об устройстве и IP.
        :return: Кортеж с refresh токеном и access токеном.
        :raises UserNotFoundError: Если пользователь не найден.
        :raises InvalidPasswordError: Если пароль неверный.
        """

        async with self._uow as uow:
            user = await uow.users.get_by_filters(email=email)
            if user is None:
                raise UserNotFoundError
            if not verify_password(password=password, hashed_password=user.password):
                raise InvalidPasswordError
            user_data = AuthService._generate_user_data(user=user)
            refresh_token, access_token = self._token_factory.create_pair(user_data)
            session = AuthService._generate_session_data(
                user=user, user_data=user_data, headers=headers
            )
            await uow.sessions.add(session)
            return refresh_token, access_token

    async def logout(self, jti: str):
        async with self._uow as uow:
            session = await uow.sessions.get_by_filters(jti=jti)
            if session is None:
                pass
            session.is_active = False
            await uow.sessions.update(object_id=session.id, model=session)
            await self._black_list.set_in_black_list(jti=jti)

        pass

    async def change_password(self, token: str, current_password: str, new_password):
        pass

    @staticmethod
    def _generate_user_data(user: User) -> Payload:
        """
        Генерация данных для токена на основе пользователя.

        :param user: Объект пользователя.
        :return: Данные токена в виде модели TokenUserData.
        """
        permissions = (
            [permission.slug for permission in user.role.permissions]
            if user.role is not None
            else []
        )
        return Payload(
            sub=str(user.id),
            scope=permissions,
            iat=datetime.utcnow(),
            exp=datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS),
            jti=str(uuid.uuid4()),
        )

    @staticmethod
    def _generate_session_data(
        user: User, user_data: Payload, headers: dict[str, Any]
    ) -> SessionCreate:
        """
        Генерация данных для сессии пользователя.

        :param user: Объект пользователя.
        :param user_data: Данные токена пользователя.
        :param headers: Заголовки запроса для извлечения информации об устройстве и IP.
        :return: Данные сессии в виде модели SessionCreate.
        """
        DEVICE_HEADER = "user-agent"
        IP_HEADER = "host"

        device = headers.get(DEVICE_HEADER, "unknown")
        ip = headers.get(IP_HEADER, "unknown")
        return SessionCreate(
            user_id=user.id,
            device=device,
            location=ip,
            jti=user_data.jti,
            expires_at=user_data.exp,
        )


@lru_cache
def get_auth_service(
    uow: IAuthUoW = Depends(get_auth_uow),
    token_factory: TokenFactory = Depends(get_token_factory),
    black_list: IBlackList = Depends(get_black_list_service),
) -> IAuthService:
    """
    Провайдер сервиса аутентификации для зависимостей.

    :param uow: Единица работы (Unit of Work) для управления транзакциями.
    :param token_factory: Фабрика токенов для создания JWT.
    :return: Экземпляр AuthService.
    """
    return AuthService(uow=uow, token_factory=token_factory, black_list=black_list)
