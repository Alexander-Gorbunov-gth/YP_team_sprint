from functools import lru_cache

from redis.asyncio import Redis
from fastapi import Depends

from src.core.config import settings
from src.db.redis import get_redis
from src.services.authhh.interfaces import IBlackList


class BlackList(IBlackList):
    def __init__(self, redis: Redis):
        """
        Инициализирует соединение с Redis.

        :param redis: Объект подключения к Redis
        """

        self._redis = redis

    async def set_in_black_list(self, jti: str, ttl: int | None = None) -> None:
        """
        Добавляет идентификатор токена (JTI) в черный список.

        :param jti: Уникальный идентификатор токена (JTI).
        :param ttl: Время жизни записи в секундах. Если None, значение будет браться из настроек.
        """

        if ttl is None:
            ttl = settings.service.access_token_expire
        await self._redis.set(jti, "blacklist", ex=ttl * 60)

    async def check_id_in_black_list(self, jti: str) -> bool:
        """
        Проверяет, находится ли идентификатор токена (JTI) в черном списке.

        :param jti: Уникальный идентификатор токена (JTI).
        :return: True, если идентификатор в черном списке, иначе False.
        """

        result = await self._redis.get(jti)
        return result is not None


@lru_cache
def get_black_list_service(redis: Redis = Depends(get_redis)):
    """
    Создает экземпляр сервиса BlackList

    :redis: экземпляр подключения к Redis
    """
    
    black_list_service = BlackList(redis=redis)
    return black_list_service
