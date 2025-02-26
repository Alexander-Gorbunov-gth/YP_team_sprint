import uuid
import logging
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext

from src.domain.entities import User, Token
from src.domain.exceptions import WrongOldPassword, WrongEmailOrPassword
from src.domain.repositories import AbstractUserRepository

logger = logging.getLogger(__name__)


class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_lifetime: timedelta = timedelta(minutes=15),
        refresh_token_lifetime: timedelta = timedelta(days=60),
    ) -> None:
        """
        Инициализирует JWT сервис с заданными параметрами.

        :param secret_key: Секретный ключ для подписи токенов.
        :param algorithm: Алгоритм шифрования (по умолчанию "H256").
        :param access_token_lifetime: Время жизни access токена.
        :param refresh_token_lifetime: Время жизни refresh токена.
        """

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime
        self.jti = str(uuid.uuid4())

    def _generate_token(self, user: User, token_lifetime: timedelta) -> str:
        """
        Генерирует JWT токен для указанного пользователя с заданным временем жизни.

        :param user: Объект пользователя, для которого создаётся токен.
        :param token_lifetime: Время жизни токена.
        :return: Сгенерированный JWT токен в виде строки.
        """

        now = datetime.now()
        payload = {
            "user_uuid": user.id,
            "iat": now.timestamp(),
            "exp": (now + token_lifetime).timestamp(),
            "jti": self.jti,
            "scope": [],
        }
        return jwt.encode(payload=payload, key=self.secret_key, algorithm=self.algorithm)

    def generate_access_token(self, user: User) -> str:
        """
        Генерирует access токен для указанного пользователя.

        :param user: Объект пользователя, для которого создаётся access токен.
        :return: Сгенерированный access JWT токен в виде строки.
        """

        return self._generate_token(user=user, token_lifetime=self.access_token_lifetime)

    def generate_refresh_token(self, user: User) -> str:
        """
        Генерирует refresh токен для указанного пользователя.

        :param user: Объект пользователя, для которого создаётся refresh токен.
        :return: Сгенерированный refresh JWT токен в виде строки.
        """

        return self._generate_token(user=user, token_lifetime=self.refresh_token_lifetime)

    def decode_token(self, jwt_token: str) -> Token:
        """
        Декодирует и валидирует JWT токен.

        :param jwt_token: JWT токен в виде строки.
        :return: Объект Token с полезной нагрузкой из токена.
        :raises jwt.ExpiredSignatureError: Если токен просрочен.
        :raises jwt.PyJWTError: Если произошла ошибка при декодировании токена.
        """

        try:
            payload = jwt.decode(jwt=jwt_token, key=self.secret_key, algorithms=[self.algorithm])
            token = Token(**payload)
        except jwt.ExpiredSignatureError:
            logger.error("Токен %s просрочен.", jwt_token)
            raise
        except (jwt.PyJWTError, TypeError):
            logger.error("Ошибка декодирования токена %s", jwt_token)
            raise jwt.PyJWTError
        return token


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self._user_repository: AbstractUserRepository = user_repository
        self._context: CryptContext = CryptContext(schemes=["bcrypt"])

    async def registration_new_user(self, email: str, password: str) -> User:
        """
        Регистрирует нового пользователя, хешируя его пароль перед сохранением.

        :param email: Email пользователя.
        :param password: Открытый пароль пользователя.
        :return: Созданный объект User.
        """
        
        hashed_password = self._get_password_hash(password)
        new_user = await self._user_repository.create(email=email, password=hashed_password)
        return new_user

    async def login_user(self, email: str, password: str) -> bool:
        """
        Проверяет учетные данные пользователя при входе.

        :param email: Email пользователя.
        :param password: Открытый пароль пользователя.
        :return: True, если аутентификация успешна.
        :raises WrongEmailOrPassword: Если учетные данные неверны.
        """

        user = await self._user_repository.get_by_email(email=email)
        if user is None or not self._verify_password(password, user.password):
            logger.error("Неверный логин для пользователя %s", email)
            raise WrongEmailOrPassword
        return True
    
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> User:
        """
        Изменяет пароль пользователя.

        :param user_id: Идентификатор пользователя.
        :param old_password: Старый пароль пользователя.
        :param new_password: Новый пароль пользователя.
        :return: Обновленный объект User.
        :raises WrongOldPassword: Если старый пароль неверен.
        """

        user = await self._user_repository.get_by_id(user_id=user_id)
        if not self._verify_password(old_password, user.password):
            logger.error("Неверный пароль для пользоавтеля %s.", str(user.id))
            raise WrongOldPassword
        hashed_new_password = self._get_password_hash(new_password)
        user.password = hashed_new_password
        updated_user = await self._user_repository.update(user=user)
        return updated_user

    def _get_password_hash(self, password) -> str:
        """
        Генерирует хеш пароля с использованием bcrypt.

        :param password: Открытый пароль.
        :return: Захешированный пароль.
        """

        return self._context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Проверяет соответствие пароля и его хеша.

        :param password: Открытый пароль.
        :param hashed_password: Захешированный пароль.
        :return: True, если пароль корректен.
        """

        return self._context.verify(password, hashed_password)
