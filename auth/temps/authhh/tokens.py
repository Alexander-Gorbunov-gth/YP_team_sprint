from datetime import datetime, timedelta
import logging

import jwt
from pydantic import ValidationError

from src.schemas.users import Payload, RefreshToken, TokenResponse
from src.core.config import settings

ACCESS_EXPIRE_MINUTES = settings.service.access_token_expire
REFRESH_EXPIRE_DAYS = settings.service.refresh_token_expire

logger = logging.getLogger(__name__)


class TokenFactory:
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_token(self, user_data: Payload, exp_time: datetime) -> str:
        to_encode = user_data.model_dump()
        to_encode["exp"] = exp_time
        token = jwt.encode(
            to_encode,
            self._secret_key,
            algorithm=self._algorithm,
        )
        return token

    def create_pair(self, user_data: Payload) -> tuple[RefreshToken, TokenResponse]:
        refresh_token = RefreshToken(
            refresh_token=self.create_token(
                user_data,
                exp_time=datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS),
            )
        )
        access_token = TokenResponse(
            access_token=self.create_token(
                user_data,
                exp_time=datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES),
            )
        )
        return refresh_token, access_token


def decode_token(token: str) -> Payload:
    """
    Декодирует JWT токен и валидирует его содержимое.

    :param token: JWT токен для декодирования.
    :return: Объект TokenUserData.
    :raises jwt.ExpiredSignatureError: Если токен истёк.
    :raises jwt.PyJWTError: Если токен некорректен.
    :raises ValidationError: Если структура токена не соответствует TokenUserData.
    """
    try:
        payload = jwt.decode(
            token,
            settings.service.secret_key.get_secret_value(),
            algorithms=[settings.service.jwt_algorithm],
        )
        return Payload(**payload)
    except jwt.ExpiredSignatureError:
        logger.error("Время жизни токена '%s' истекло", token)
        raise
    except jwt.PyJWTError:
        logger.error("Подпись токена '%s' недействительна.", token)
        raise
    except ValidationError as e:
        logger.error("Некорректные данные в токене '%s': %s", token, e)
        raise


def get_token_factory() -> TokenFactory:
    token_factory = TokenFactory(
        secret_key=settings.service.secret_key.get_secret_value(),
        algorithm=settings.service.jwt_algorithm,
    )
    return token_factory
