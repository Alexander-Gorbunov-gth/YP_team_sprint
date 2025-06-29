from abc import ABC, abstractmethod
from typing import Any


class AbstractProducer(ABC):
    @abstractmethod
    async def send(self, message: dict[str, Any], routing_key: str, delay_ms: int | None = None) -> None: ...
