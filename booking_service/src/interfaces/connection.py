from abc import ABC, abstractmethod


class AbstractConnection(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
