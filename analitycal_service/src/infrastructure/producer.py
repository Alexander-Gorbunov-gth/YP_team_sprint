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
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="PLAIN",
            sasl_plain_username=username,
            sasl_plain_password=password,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),  # сериализация dict в JSON
            key_serializer=lambda v: v.encode("utf-8"),  # сериализация ключа (строка → байты)
        )

    async def start(self):
        """Устанавливаем соединение с Kafka и запускаем фоновые задачи продюсера"""
        await self._producer.start()

    async def stop(self):
        """Завершаем соединение и останавливаем фоновые задачи"""
        await self._producer.stop()

    async def send_message(self, topic: str, value: dict, key: str | None = None):
        """Отправляем сообщение в Kafka (асинхронно, без ожидания подтверждения)"""
        await self._producer.send(topic=topic, value=value, key=key)

    async def send_message_and_wait(self, topic: str, value: dict, key: str | None = None):
        """Отправляем сообщение и дожидаемся подтверждения от брокера"""
        await self._producer.send_and_wait(topic=topic, value=value, key=key)


# Глобальный экземпляр — для внедрения DI
producer: AbstractProducerBroker | None = None


def get_producer() -> Optional[AbstractProducerBroker]:
    return producer
