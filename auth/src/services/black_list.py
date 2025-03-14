from datetime import timedelta

from fastapi import Depends

from src.domain.interfaces import AbstractBlackListService
from src.domain.repositories import AbstractBlackListRepository
from src.infrastructure.repositories.black_list import get_black_list_repository


class BlackListService(AbstractBlackListService):
    """Сервис для работы с черным списком токенов."""

    def __init__(self, black_list_repository: AbstractBlackListRepository):
        """
        Инициализация сервиса.
        :param black_list_repository: Репозиторий черного списка (реализация хранилища).
        """
        self._repository = black_list_repository

    async def is_exists(self, key: str) -> bool:
        """
        Проверяет, существует ли ключ в черном списке.
        :param key: Ключ (например, идентификатор токена).
        :return: True, если ключ существует, иначе False.
        """

        value = await self._repository.get_value(key=key)
        return value is not None

    async def set_one_value(self, key: str, value: str, exp: timedelta | None = None):
        """
        Добавляет один ключ в черный список.
        :param key: Ключ (например, идентификатор токена).
        :param value: Значение, связанное с ключом.
        :param exp: Время жизни ключа (если не указано, ключ будет без срока действия).
        """

        await self._repository.set_value(key=key, value=value, exp=exp)

    async def set_many_values(self, values: list[dict[str, str]], exp: timedelta | None = None):
        """
        Добавляет несколько значений в хранилище.
        :param values: Словарь {ключ: значение}.
        :param exp: Время жизни ключей (если указано, будет установлено время истечения).
        """
        await self._repository.set_many_values(values=values, exp=exp)


def get_black_list_service(
    repository: AbstractBlackListRepository = Depends(get_black_list_repository),
) -> AbstractBlackListService:
    """
    Фабричный метод для получения экземпляра BlackListService.
    :param repository: Репозиторий черного списка.
    :return: Экземпляр сервиса черного списка.
    """
    black_list_service = BlackListService(repository)
    return black_list_service
