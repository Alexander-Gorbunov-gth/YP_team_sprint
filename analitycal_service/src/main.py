import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio.client import Redis

from src.db import redis
from src.api.v1.event import route
from src.core.config import settings
from src.infrastructure import consumer, producer
from src.services.consumer_handlers import AuthConsumerHandler


@asynccontextmanager
async def lifespan(_: FastAPI):
    producer.producer = producer.KafkaProducerWrapper(
        bootstrap_servers=settings.brocker.bootstrap_service,
        username=settings.brocker.kafka_username,
        password=settings.brocker.kafka_password,
    )
    consumer.consumer = consumer.KafkaConsumerWrapper(
        bootstrap_servers=settings.brocker.bootstrap_service,
        username=settings.brocker.kafka_username,
        password=settings.brocker.kafka_password,
        topics=settings.brocker.consumer_topics,
        group_id=settings.brocker.consumer_group_id,
    )
    consumer.consumer.register_handler(settings.brocker.auth_topic_name, AuthConsumerHandler().handle)
    await producer.producer.start()
    task = asyncio.create_task(consumer.consumer.start())

    redis.redis = Redis.from_url(settings.redis.redis_url)

    yield

    await producer.producer.stop()
    await consumer.consumer.stop()
    task.cancel()

    await redis.redis.close()


app = FastAPI(
    debug=settings.service.debug,
    title=settings.service.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/apenapi.json/",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)


app.include_router(router=route, prefix="/api/v1")


if __name__ == "__main__":
    app()
