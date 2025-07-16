from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import root

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient
from src.api.v1.router import router as api_router
from src.core.config import settings
#from src.infrastructure.clients import http



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    
    # http.httpx_client = AsyncClient(timeout=5.0)

    yield

    #await http.httpx_client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.proect.title,
        description=settings.proect.decription,
        debug=settings.proect.debug,
        lifespan=lifespan,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        response_class=ORJSONResponse,
        root_path="/proxy/8000/",
    )
    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    app()
