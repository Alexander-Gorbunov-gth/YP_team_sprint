from abc import ABC, abstractmethod


from src.domain.entities import User, Token


class AbstractJWTService(ABC):
    @abstractmethod
    def generate_access_token(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_refresh_token(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, jwt_token: str) -> Token:
        raise NotImplementedError


class AbstractAuthService(ABC):
    @abstractmethod
    async def registration_new_user(self, email: str, password: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    async def login_user(self, email: str, password: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> User:
        raise NotImplementedError
