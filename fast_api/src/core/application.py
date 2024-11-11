# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# # from src.core.config import get_settings


# async def _include_routers(app: FastAPI) -> None:
#     app.include_router(root_router)
#     app.include_router(auth_router)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("🚀 Starting application")
#     await _include_routers(app)
#     yield
#     logger.info("⛔ Stopping application")