from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.router import router as api_router
from src.core.config import settings
from src.infrastructure.container import AppContainer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await AppContainer.startup(app=app)

    try:
        yield
    finally:
        await AppContainer.shutdown()


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
