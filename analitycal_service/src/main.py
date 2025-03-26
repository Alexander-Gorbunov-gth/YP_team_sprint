from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.infrastructure import producer


@asynccontextmanager
async def lifespan(_, app: FastAPI):
    producer.producer = producer.KafkaProducerWrapper(
        bootstrap_servers=settings.producer.bootstrap_service,
        username=settings.producer.kafka_username,
        password=settings.producer.kafka_password,
    )
    producer.producer.start()

    yield

    producer.producer.stop()


app = FastAPI(
    debug=True,
    title="Test",
    description="Test",
    docs_url="/api/openapi/",
    openapi_url="/api/apenapi.json/",
    lifespan=lifespan,
)


if __name__ == "__main__":
    app()
