import logging
import string
from json import JSONDecodeError
from secrets import choice as secrets_choice
from urllib.parse import urlencode

from fastapi import Depends
from httpx import AsyncClient
from passlib.context import CryptContext

from src.core.config import settings
from src.core.http_client import get_http_client
from src.domain.entities import SocialAccount, User
from src.domain.exceptions import (
    OAuthAccessTokenNotFound,
    OAuthResponseDecodeError,
    OAuthTokenExchangeError,
    OAuthUserInfoError,
)
from src.domain.interfaces import AbstractOAuthService
from src.infrastructure.repositories.user import get_user_repository
from src.infrastructure.repositories.social_account import get_social_account_repository
from src.domain.repositories import AbstractSocialAccountRepository, AbstractUserRepository

logger = logging.getLogger(__name__)



class YandexOAuthService(AbstractOAuthService):
    YANDEX_OAUTH_AUTHORIZE_URL = "https://oauth.yandex.ru/authorize"
    YANDEX_OAUTH_TOKEN_URL = "https://oauth.yandex.ru/token"
    YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"
    SCOPE = "login:email login:info"
    SOCIAL_NAME = "yandex"

    def __init__(
        self,
        http_client: AsyncClient,
        social_repository: AbstractSocialAccountRepository,
        user_repository: AbstractUserRepository,
    ):
        self._client = http_client
        self._social_repository: AbstractSocialAccountRepository = social_repository
        self._user_repository: AbstractUserRepository = user_repository
        self._context: CryptContext = CryptContext(schemes=["bcrypt"])

    async def get_oauth_url(self) -> str:
        """
        Генерирует URL для перенаправления пользователя на страницу авторизации Яндекса.
        :return: Полный URL авторизации
        """
        params = {
            "response_type": "code",
            "client_id": settings.oauth.yandex_client_id,
            "redirect_uri": settings.oauth.yandex_callback_url,
            "scope": self.SCOPE,
        }
        url = f"{self.YANDEX_OAUTH_AUTHORIZE_URL}?{urlencode(params)}"
        logger.debug("Generated Yandex OAuth URL: %s", url)
        return url

    async def _get_oauth_token(self, code: str) -> str:
        """
        Получает access_token от Яндекса по коду авторизации.
        :param code: Код авторизации, полученный от Яндекса
        :return: access_token
        :raises: OAuthTokenExchangeError, OAuthResponseDecodeError, OAuthAccessTokenNotFound
        """
        request_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.oauth.yandex_client_id,
            "client_secret": settings.oauth.yandex_client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = await self._client.post(url=self.YANDEX_OAUTH_TOKEN_URL, data=request_data, headers=headers)

        if response.status_code != 200:
            logger.error("Ошибка при полчении access_token: status=%s, body=%s", response.status_code, response.text)
            raise OAuthTokenExchangeError

        try:
            token_data = response.json()
        except JSONDecodeError as e:
            logger.exception("Ошибка декодирования ответа при получении access_token")
            raise OAuthResponseDecodeError from e

        access_token = token_data.get("access_token")
        if access_token is None:
            logger.error("access_token не найден в ответе: %s", token_data)
            raise OAuthAccessTokenNotFound

        logger.info("Успешно получен access_token")
        return access_token

    async def _get_user_info(self, code: str) -> dict[str, str]:
        """
        Получает информацию о пользователе от Яндекса используя access_token.
        :param code: Код авторизации от Яндекса
        :return: Словарь с информацией о пользователе
        :raises: OAuthUserInfoError, OAuthResponseDecodeError
        """
        access_token = await self._get_oauth_token(code)
        headers = {"Authorization": f"OAuth {access_token}"}
        params = {"format": "json"}

        response = await self._client.get(url=self.YANDEX_USER_INFO_URL, headers=headers, params=params)

        if response.status_code != 200:
            logger.error("Ошибка при получении user_info: status=%s, body=%s", response.status_code, response.text)
            raise OAuthUserInfoError

        try:
            user_info = response.json()
        except JSONDecodeError as e:
            logger.exception("Ошибка декодирования ответа user_info")
            raise OAuthResponseDecodeError from e

        logger.info("Успешно получены данные пользователя от Яндекса")
        return user_info

    async def create_user_by_social_account(self, code: str) -> User:
        """Создание или получение пользователя и привязка соц. аккаунта."""
        client_id, user_email = await self._validate_user_info(code=code)
        user, created = await self._get_or_create_user(email=user_email)
        if not created:
            social_account = SocialAccount(
                id=None,
                client_id=client_id,
                user_id=user.id,
                social_name=self.SOCIAL_NAME,
            )
            await self._social_repository.save_social_account(social_account=social_account)
        return user

    async def _get_or_create_user(self, email: str) -> tuple[str, bool]:
        """
        Получить пользователя из БД или создать нового.
        Возвращает кортеж (пользователь, был_ли_создан).
        """
        hashed_password = self._get_password_hash()
        created = False
        user = await self._user_repository.get_by_email(email=email)
        if user is None:
            logger.info("Пользователь с email '%s' уже существует", email)
            user = await self._user_repository.create(email=email, password=hashed_password)
            created = True
        return user, created

    async def _validate_user_info(self, code: str) -> tuple[str, str]:
        """Извлекает client_id и email из user_info."""
        user_info = await self._get_user_info(code=code)
        user_email = user_info.get("default_email")
        if user_email is None:
            logger.error("Email пользователя не найден, code=%s", code)
            raise OAuthResponseDecodeError
        client_id = user_info.get("client_id")
        if client_id is None:
            logger.error("client_id не найден, code=%s", code)
            raise OAuthResponseDecodeError
        return client_id, user_email

    def _get_password_hash(self) -> str:
        """
        Генерирует пароль и его хэш с использованием bcrypt.
        :return: Захешированный пароль.
        """
        alphabet = string.ascii_letters + string.digits
        random_password = ''.join(secrets_choice(alphabet) for _ in range(16)) 
        return self._context.hash(random_password)


def get_yandex_oauth_service(
    http_client: AsyncClient = Depends(get_http_client),
    social_repository: AbstractSocialAccountRepository = Depends(get_social_account_repository),
    user_repository: AbstractUserRepository = Depends(get_user_repository),
) -> AbstractOAuthService:
    return YandexOAuthService(
        http_client=http_client,
        social_repository=social_repository,
        user_repository=user_repository,
    )
