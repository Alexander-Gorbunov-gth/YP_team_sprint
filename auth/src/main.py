from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from fastapi.middleware.cors import CORSMiddleware


from src.api.v1 import v1_router
from src.core import http_client
from src.core.config import settings
from src.core.exception_handlers import exception_handlers
from src.core.middlewares import RateLimiterMiddleware, RequestIdMiddleware
from src.db import postgres, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    http_client.http_client = AsyncClient()
    redis.redis = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
    postgres.engine = create_async_engine(settings.db.db_url)
    postgres.async_session_maker = async_sessionmaker(
        bind=postgres.engine, expire_on_commit=False, class_=AsyncSession
    )

    yield

    await http_client.http_client.aclose()
    await redis.redis.close()


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: "auth-service"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.jaeger.host,
                agent_port=settings.jaeger.port,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


app = FastAPI(
    title=settings.service.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json/",
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)

if settings.jaeger.enable_tracer:
    configure_tracer()
    app.add_middleware(RequestIdMiddleware)

app.add_middleware(
    RateLimiterMiddleware,
    limit=settings.service.rate_limit,
    window=settings.service.rate_window,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


FastAPIInstrumentor.instrument_app(app=app)


app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    app()
