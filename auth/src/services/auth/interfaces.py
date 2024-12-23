from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta


Model = TypeVar("Model", bound=DeclarativeMeta)


class IAuthService(ABC):
    @abstractmethod
    async def register(self, *args, **kwargs):
        """Регистрирует нового пользователя в системе."""

        raise NotImplementedError

    # @abstractmethod
    # async def login(self, *args, **kwargs):
    #     """Выполняет вход пользователя по электронной почте и паролю."""
    #
    #     raise NotImplementedError

    # @abstractmethod
    # async def change_password(self, *args, **kwargs):
    #     """Изменяет пароль пользователя."""

    #     raise NotImplementedError

    # @abstractmethod
    # async def logout(self, *args, **kwargs):
    #     """Выполняет выход пользователя из системы, аннулирует сессию."""
    #
    #     raise NotImplementedError

    # @abstractmethod
    # async def refresh(self, *args, **kwargs):
    #     """Обновляет токен доступа с использованием refresh-токена."""

    #     raise NotImplementedError

    # @abstractmethod
    # async def close_sessions(self):
    #     """Закрывает все активные сессии пользователя, кроме текущей."""

    #     raise NotImplementedError


class IRepository(ABC):
    """
    Интерфейс репозитория, определяющий основные методы для работы с данными.
    Этот интерфейс может быть реализован для различных типов хранилищ (SQL, NoSQL, файловые системы и т.д.).
    """

    @abstractmethod
    async def add(self, *args, **kwargs):
        """
        Асинхронный метод для добавления объекта в хранилище.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        """
        Асинхронный метод для обновления объекта в хранилище.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        """
        Асинхронный метод для получения объекта из хранилища по его идентификатору.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        """
        Асинхронный метод для получения списка объектов из хранилища.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """
        Асинхронный метод для удаления объекта из хранилища.
        Должен быть реализован в подклассе.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_filters(self, *args, **kwargs):
        """
        Асинхронный метод для получения списка объектов из хранилища, который удовлетворяют условиям.
        Должен быть реализован в подклассе.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_with_joins(self, *args, **kwargs):
        """
        Асинхронный метод для получения списка объектов из нескольких таблиц хранилища.
        Должен быть реализован в подклассе.
        """

        raise NotImplementedError


class ISQLAlchemyRepository(IRepository, ABC):
    """
    Базовый класс SQL-репозитория, предоставляющий общую функциональность для работы с SQLAlchemy.
    """

    def __init__(self, session: AsyncSession, model: Model) -> None:
        """
        Инициализирует SQL-репозиторий.

        Args:
            db_session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных.
            model: Модель базы данных (ORM-класс), с которой будет работать репозиторий.
        """
        self._session: AsyncSession = session
        self._model: Model = model


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


class IAuthUoW(IBaseUoW, ABC):
    """Интерфейс UoW для сервиса аутентификации"""

    users: ISQLAlchemyRepository
    sessions: ISQLAlchemyRepository
    roles: ISQLAlchemyRepository
    permissions: ISQLAlchemyRepository


class IBlackList(ABC):
    """
    Абстрактный класс для работы с черным списком токенов (JTI).
    """

    @abstractmethod
    async def set_in_black_list(self, jti: str, ttl: int | None = None) -> None:
        """
        Добавляет идентификатор токена (JTI) в черный список.

        :param jti: Уникальный идентификатор токена (JTI).
        :param ttl: Время жизни записи в черном списке в секундах.
                    Если None, запись будет храниться бесконечно.
        """
        raise NotImplementedError

    @abstractmethod
    async def check_id_in_black_list(self, jti: str) -> bool:
        """
        Проверяет, находится ли идентификатор токена (JTI) в черном списке.

        :param jti: Уникальный идентификатор токена (JTI).
        :return: True, если идентификатор находится в черном списке, иначе False.
        """
        raise NotImplementedError
