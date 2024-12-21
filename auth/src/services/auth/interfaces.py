from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

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


class IBaseUoW(ABC):
    """
    Интерфейс для любых единиц работы,
    которые будут использоваться для атомарности транзакций, согласно DDD.
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            await self._commit()
        else:
            await self._rollback()

    @abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError


class ISQLAlchemyUoW(IBaseUoW):
    """Реализация Unit of Work для работы с базой данных через SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация Unit of Work с асинхронной сессией.

        Args:
            session_factory [AsyncSession]: Асинхронныя сессия SQLAlchemy.
        """

        super().__init__()
        self._session: AsyncSession = session

    async def __aenter__(self) -> "ISQLAlchemyUoW":
        """
        Открытие контекста Unit of Work, создавая новую сессию.

        Returns:
            SQLAlchemyAbstractUnitOfWork: Текущий экземпляр.
        """

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Завершение контекста Unit of Work и закрытие сессии."""
        await super().__aexit__(exc_type, exc_value, traceback)
        await self._session.close()

    async def _commit(self) -> None:
        """Зафиксировать изменения в базе данных."""

        await self._session.commit()

    async def _rollback(self) -> None:
        """Откатить изменения в базе данных."""

        self._session.expunge_all()
        await self._session.rollback()
