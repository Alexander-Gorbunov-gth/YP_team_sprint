from abc import ABC, abstractmethod

from src.models.users import User
from src.services.users.schemas import UserCreate
from src.services.auth.schemas import ResponseTokens


class IAuthService(ABC):
    @abstractmethod
    async def register(self, user: UserCreate) -> User:
        """
        Регистрирует нового пользователя в системе.

        :param user: Информация о пользователе, которую нужно зарегистрировать.
        :return: Модель пользователя, содержащая данные о новом пользователе.
        """
        raise NotImplementedError

    @abstractmethod
    async def login(self, email: str, password: str) -> ResponseTokens:
        """
        Выполняет вход пользователя по электронной почте и паролю.

        :param email: Электронная почта пользователя.
        :param password: Пароль пользователя.
        :return: Токены, содержащие доступ к системе.
        """
        raise NotImplementedError

    @abstractmethod
    async def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> User:
        """
        Изменяет пароль пользователя.

        :param access_token: Токен доступа пользователя для завершения сессии.
        :param current_password: Текущий пароль пользователя.
        :param new_password: Новый пароль, который нужно установить.
        :return: Модель пользователя с обновленным паролем.
        """
        raise NotImplementedError

    @abstractmethod
    async def logout(self, access_token: str):
        """
        Выполняет выход пользователя из системы, аннулирует сессию.

        :param access_token: Токен доступа пользователя для завершения сессии.
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, refresh_token: str) -> ResponseTokens:
        """
        Обновляет токен доступа с использованием refresh-токена.

        :param refresh_token: Токен обновления для получения нового access-токена.
        :return: Новая пара ключей.
        """
        raise NotImplementedError

    @abstractmethod
    async def close_sessions(self, current_user_id: str, current_access_token: str):
        """
        Закрывает все активные сессии пользователя, кроме текущей.

        :param current_access_token: Текущий токен пользователя, который не должен быть закрыт.
        :return: None
        """
        raise NotImplementedError
