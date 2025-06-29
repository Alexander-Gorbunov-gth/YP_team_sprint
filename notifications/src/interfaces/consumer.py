from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    @abstractmethod
    async def connect(self) -> None: ...
