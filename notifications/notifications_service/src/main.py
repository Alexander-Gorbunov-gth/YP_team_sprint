from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient

from src.core.config import settings
from src.consumers.incoming_tasks import start_incomming_task_consumer
from src.producers.producer import RabbitMQPublisher
from src.infrastructure.connections import http

from src.producers import global_publisher


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:

    publisher = RabbitMQPublisher(settings.rabbit.rabbit_url)
    await publisher.connect()
    global_publisher.publisher = publisher
    incoming_tasks_connection = await start_incomming_task_consumer()
    http.httpx_client = AsyncClient(timeout=5.0)
    try:
        yield
    finally:
        await incoming_tasks_connection.close()
        await publisher.close()
        await http.httpx_client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.proect.title,
        description=settings.proect.decription,
        debug=settings.proect.debug,
        lifespan=lifespan,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        response_class=ORJSONResponse,
    )
    # app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    app()
