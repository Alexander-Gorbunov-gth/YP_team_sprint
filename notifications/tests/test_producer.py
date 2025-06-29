#!/usr/bin/env python3

from src.infrastructure.messaging.producer import RabbitMQProducer
from src.interfaces.connection import AbstractConnection
from src.services.interfaces.messaging.producer import AbstractProducer

print("Testing RabbitMQProducer...")

# Проверяем наследование
print(f"Is RabbitMQProducer subclass of AbstractProducer: {issubclass(RabbitMQProducer, AbstractProducer)}")
print(f"Is RabbitMQProducer subclass of AbstractConnection: {issubclass(RabbitMQProducer, AbstractConnection)}")

# Проверяем методы
print(f"Has send method: {hasattr(RabbitMQProducer, 'send')}")
print(f"Has connect method: {hasattr(RabbitMQProducer, 'connect')}")
print(f"Has close method: {hasattr(RabbitMQProducer, 'close')}")

# Проверяем, что методы не абстрактные
import inspect

print(f"send is abstract: {inspect.isabstract(RabbitMQProducer.send)}")
print(f"connect is abstract: {inspect.isabstract(RabbitMQProducer.connect)}")
print(f"close is abstract: {inspect.isabstract(RabbitMQProducer.close)}")

# Пытаемся создать экземпляр
try:
    producer = RabbitMQProducer("amqp://localhost", "test")
    print("✅ Instance created successfully!")
except Exception as e:
    print(f"❌ Error creating instance: {e}")
    print(f"Error type: {type(e)}")
