from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.v1.router import router
from src.infrastructure.container import Container
from src.infrastructure.lifetime import AppLifetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_lifetime = AppLifetime()
    await app_lifetime.startup()
    try:
        yield
    finally:
        await app_lifetime.shutdown()
        await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router, prefix="/api")
    container = make_async_container(Container())
    setup_dishka(container=container, app=app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
