from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import router
from src.infrastructure.container import Container
from src.infrastructure.lifetime import AppLifetime


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    app_lifetime = AppLifetime()
    await app_lifetime.startup()
    try:
        yield
    finally:
        await app_lifetime.shutdown()
        await fastapi_app.state.dishka_container.close()



def create_app() -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan, docs_url="/api/openapi", openapi_url="/api/openapi.json")
    fastapi_app.include_router(router, prefix="/api")
    container = make_async_container(Container())
    setup_dishka(container=container, app=fastapi_app)
    return fastapi_app


app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
