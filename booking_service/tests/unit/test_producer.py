import asyncio

from src.infrastructure.messaging.producer import RabbitMQProducer
from src.interfaces.connection import AbstractConnection
from src.services.interfaces.producer import IProducer, PublishMessage

print("Testing RabbitMQProducer...")

# Проверяем наследование
print(f"Is RabbitMQProducer subclass of AbstractProducer: {issubclass(RabbitMQProducer, IProducer)}")
print(f"Is RabbitMQProducer subclass of AbstractConnection: {issubclass(RabbitMQProducer, AbstractConnection)}")

# Проверяем методы
print(f"Has publish method: {hasattr(RabbitMQProducer, 'publish')}")
print(f"Has connect method: {hasattr(RabbitMQProducer, 'connect')}")
print(f"Has close method: {hasattr(RabbitMQProducer, 'close')}")

# Проверяем, что методы не абстрактные
import inspect

print(f"publish is abstract: {inspect.isabstract(RabbitMQProducer.publish)}")
print(f"connect is abstract: {inspect.isabstract(RabbitMQProducer.connect)}")
print(f"close is abstract: {inspect.isabstract(RabbitMQProducer.close)}")

# Пытаемся создать экземпляр
try:
    producer = RabbitMQProducer("amqp://rabbitmq_user:rabbitmq_password@127.0.0.1:5672/", "test")
    print("✅ Instance created successfully!")
except Exception as e:
    print(f"❌ Error creating instance: {e}")
    print(f"Error type: {type(e)}")


# Пытаемся отправить сообщение
async def send_message():
    try:
        await producer.connect()
        print("✅ Connection established successfully!")

        await producer.publish(
            message=PublishMessage(
                event_type="test_event",
                channels=["email"],
                for_all_users=False,
                user_params=None,
                send_in_local_time=False,
                send_at=None,
            ),
            routing_key="test_routing_key",
            delay_ms=1000,
        )
        print("✅ Message published successfully!")

    except Exception as e:
        print(f"❌ Error connecting: {e}")
        print(f"Error type: {type(e)}")


asyncio.run(send_message())
