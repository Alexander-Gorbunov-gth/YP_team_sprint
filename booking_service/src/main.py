from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.v1.router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
