import asyncio
import inspect

from src.infrastructure.messaging.producer import RabbitMQProducer
from src.interfaces.connection import AbstractConnection
from src.services.interfaces.producer import IProducer, PublishMessage


async def test_rabbitmq_producer():
    print("Testing RabbitMQProducer...")
    passed = True

    # Проверяем наследование
    try:
        assert issubclass(RabbitMQProducer, IProducer)
        assert issubclass(RabbitMQProducer, AbstractConnection)
        print("✅ Inheritance checks passed")
    except AssertionError:
        print("❌ Inheritance checks failed")
        passed = False

    # Проверяем методы
    try:
        assert hasattr(RabbitMQProducer, 'publish')
        assert hasattr(RabbitMQProducer, 'connect')
        assert hasattr(RabbitMQProducer, 'close')
        print("✅ Method existence checks passed")
    except AssertionError:
        print("❌ Method existence checks failed")
        passed = False

    # Проверяем, что методы не абстрактные
    try:
        assert not inspect.isabstract(RabbitMQProducer.publish)
        assert not inspect.isabstract(RabbitMQProducer.connect)
        assert not inspect.isabstract(RabbitMQProducer.close)
        print("✅ Concrete method checks passed")
    except AssertionError:
        print("❌ Concrete method checks failed")
        passed = False

    # Пытаемся создать экземпляр
    try:
        producer = RabbitMQProducer("amqp://rabbitmq_user:rabbitmq_password@127.0.0.1:5672/", "test")
        print("✅ Instance created successfully!")
    except Exception as e:
        print(f"❌ Error creating instance: {e}")
        passed = False

    # Пытаемся отправить сообщение
    if passed:
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
            passed = True
        except Exception as e:
            print(f"❌ Error in publishing: {e}")
            passed = False
        finally:
            await producer.close()

    assert passed, "Some RabbitMQProducer tests failed"

if __name__ == "__main__":
    asyncio.run(test_rabbitmq_producer())
