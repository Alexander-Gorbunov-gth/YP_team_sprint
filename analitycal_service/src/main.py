from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import settings
from src.infrastructure import brocker
from src.api.v1.event import route


@asynccontextmanager
async def lifespan(_: FastAPI):
    brocker.brocker = brocker.KafkaProducerWrapper(
        bootstrap_servers=settings.brocker.bootstrap_service,
        username=settings.brocker.kafka_username,
        password=settings.brocker.kafka_password,
    )
    await brocker.brocker.start()

    yield

    await brocker.brocker.stop()


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
