import abc
import logging

import jwt

from src.domain.entities.user import User
from src.services.exceptions import SessionHasExpired
from src.core.config import settings

logger = logging.getLogger(__name__)


class AbstractJWTService(abc.ABC):
    @abc.abstractmethod
    def decode_token(self, jwt_token: str) -> User: ...


class JWTService(AbstractJWTService):
    def __init__(
        self,
        secret_key: str = settings.auth.secret_key.get_secret_value(),
        algorithm: str = settings.auth.algorithm,
    ) -> None:
        """
        Инициализирует JWT сервис с заданными параметрами.
        :param secret_key: Секретный ключ для подписи токенов.
        :param algorithm: Алгоритм шифрования (по умолчанию "H256").
        """

        self._secret_key = secret_key
        self._algorithm = algorithm

    def decode_token(self, jwt_token: str) -> User:
        """
        Декодирует и валидирует JWT токен.

        :param jwt_token: JWT токен в виде строки.
        :return: Объект Token с полезной нагрузкой из токена.
        :raises SessionHasExpired: Если токен просрочен.
        """
        try:
            payload = jwt.decode(
                jwt=jwt_token,
                key=self._secret_key,
                algorithms=[self._algorithm],
                options={"verify_exp": False},
            )
            user = User(id=payload["user_uuid"])
        except jwt.ExpiredSignatureError as e:
            logger.error("Токен %s просрочен.", jwt_token)
            raise SessionHasExpired from e
        except (jwt.PyJWTError, TypeError) as e:
            logger.error("Ошибка декодирования токена %s", jwt_token)
            logger.error(e)
            raise SessionHasExpired from e
        return user
