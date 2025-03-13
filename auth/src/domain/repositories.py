from abc import ABC, abstractmethod
from datetime import timedelta

from src.domain.entities import User, Permission, Role


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        raise NotImplementedError


class BlackListRepository(ABC):
    @abstractmethod
    async def exists(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, token: str, expire: timedelta) -> None:
        raise NotImplementedError


class AbstractPermissionRepository(ABC):
    @abstractmethod
    async def create_permission(self, slug: str, description: str | None) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission(self, permission: Permission) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def get_permission(self, slug: str) -> Permission:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_permissions(self) -> list[Permission]:
        raise NotImplementedError
    
    @abstractmethod
    async def update_permission(self, permission: Permission) -> Permission:
        raise NotImplementedError
    

class AbstractRoleRepository(ABC):
    @abstractmethod
    async def create_role(
        self,
        slug: str,
        title: str,
        permissions: list[Permission],
        description: str | None
    ) -> Role:
        raise NotImplementedError

    @abstractmethod
    async def delete_role(self, role: Role) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def get_role(self, slug: str) -> Role:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_roles(self) -> list[Role]:
        raise NotImplementedError
    
    @abstractmethod
    async def update_role(
        self,
        role: Role
    ) -> Role:
        raise NotImplementedError
