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
    async def add_permission(self, *args, **kwargs):
        pass

    @abstractmethod
    async def remove_permission(self, *args, **kwargs):
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
    async def assign_permission_to_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def remove_permission_from_user(self, *args, **kwargs):
        pass
