import json
from abc import ABC, abstractmethod
from typing import Callable

from aiokafka import AIOKafkaConsumer


class AbstractConsumerBroker(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    def register_handler(self, topic_name: str, handler: Callable) -> None: ...


class KafkaConsumerWrapper(AbstractConsumerBroker):
    def __init__(self, bootstrap_servers: str, username: str, password: str, topics: list[str], group_id: str) -> None:
        """Инициализируем AIOKafkaProducer с авторизацией и сериализацией"""
        self._consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            key_deserializer=lambda v: v.decode("utf-8") if v else None,
            group_id=group_id,
            enable_auto_commit=True
        )
        self._handlers = {}

    def register_handler(self, topic_name: str, handler: Callable) -> None:
        self._handlers[topic_name] = handler

    async def start(self):
        """Устанавливаем соединение с Kafka и запускаем фоновые задачи продюсера"""
        await self._consumer.start()
        try:
            async for message in self._consumer:
                handler = self._handlers.get(message.topic)
                if handler:
                    await handler(message.topic, message.value, message.key)
        finally:
            await self.stop()

    async def stop(self):
        """Завершаем соединение и останавливаем фоновые задачи"""
        await self._consumer.stop()


# Глобальный экземпляр — для внедрения DI
consumer: AbstractConsumerBroker | None = None


def get_consumer() -> AbstractConsumerBroker:
    return consumer
