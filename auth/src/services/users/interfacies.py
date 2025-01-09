from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_multi(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_email(self, *args, **kwargs):
        """Метод для получения пользователя по его email."""

        raise NotImplementedError

    @abstractmethod
    async def add_role(self, *args, **kwargs):
        pass


class IUserService(ABC):
    @abstractmethod
    async def create_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_all_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def add_role_to_users(self, *args, **kwargs):
        pass


class IRoleRepository(ABC):
    @abstractmethod
    async def create(self, *args, **kwargs):
        """Создать новую роль."""
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        """Получить роль по её идентификатору."""
        pass

    @abstractmethod
    async def assign_permissions(self, *args, **kwargs):
        """Добавить разрешения к роли."""
        pass


class IRoleService(ABC):
    @abstractmethod
    async def create_role(self, *args, **kwargs):
        """Создать новую роль."""
        pass

    @abstractmethod
    async def get_role_by_id(self, *args, **kwargs):
        """Получить роль по её идентификатору."""
        pass

    @abstractmethod
    async def assign_permission(self, *args, **kwargs):
        """Назначить разрешение роли."""
        pass
