import json
from abc import ABC, abstractmethod
from typing import Optional

from aiokafka import AIOKafkaProducer


class AbstractProducerBroker(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    async def send_message(self, topic: str, value: dict, key: str | None = None): ...

    @abstractmethod
    async def send_message_and_wait(self, topic: str, value: dict, key: str | None = None): ...


class KafkaProducerWrapper(AbstractProducerBroker):
    def __init__(self, bootstrap_servers: str, username: str, password: str) -> None:
        """Инициализируем AIOKafkaProducer с авторизацией и сериализацией"""
        self._brocker = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8"),
        )

    async def start(self):
        """Устанавливаем соединение с Kafka и запускаем фоновые задачи продюсера"""
        await self._brocker.start()

    async def stop(self):
        """Завершаем соединение и останавливаем фоновые задачи"""
        await self._brocker.stop()

    async def send_message(self, topic: str, value: dict, key: str | None = None):
        """Отправляем сообщение в Kafka (асинхронно, без ожидания подтверждения)"""
        await self._brocker.send(topic=topic, value=value, key=key)

    async def send_message_and_wait(self, topic: str, value: dict, key: str | None = None):
        """Отправляем сообщение и дожидаемся подтверждения от брокера"""
        await self._brocker.send_and_wait(topic=topic, value=value, key=key)


# Глобальный экземпляр — для внедрения DI
brocker: AbstractProducerBroker | None = None


def get_brocker() -> AbstractProducerBroker:
    return brocker
