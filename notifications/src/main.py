from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.router import router as api_router
from src.consumers.email_worker import start_email_consumer
from src.consumers.incoming_tasks import start_incomming_task_consumer
from src.consumers.push_worker import start_push_consumer
from src.core.config import settings
from src.infrastructure.container import AppContainer
from src.producers import global_publisher
from src.producers.producer import RabbitMQPublisher


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await AppContainer.startup(app=app)

    rabbitmq_publisher = RabbitMQPublisher(settings.rabbit.connection_url)
    await rabbitmq_publisher.connect()
    global_publisher.publisher = rabbitmq_publisher
    incoming_tasks_connection = await start_incomming_task_consumer()
    email_connect = await start_email_consumer()
    push_connect = await start_push_consumer()
    try:
        yield
    finally:
        await AppContainer.shutdown()
        await incoming_tasks_connection.close()
        await email_connect.close()
        await push_connect.close()
        await rabbitmq_publisher.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.proect.title,
        description=settings.proect.description,
        debug=settings.proect.debug,
        lifespan=lifespan,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        response_class=ORJSONResponse,
    )
    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    app()
