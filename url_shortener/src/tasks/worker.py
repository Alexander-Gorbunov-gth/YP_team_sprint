from taskiq import TaskiqScheduler, TaskiqDepends
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisStreamBroker

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db import postgres
from src.core.config import settings
from src.services.short_url import ShortUrlService, get_short_url_service_taskqi


postgres.engine = create_async_engine(settings.db.db_url)
postgres.async_session_maker = async_sessionmaker(
    bind=postgres.engine,
    expire_on_commit=False,
    class_=AsyncSession
)

broker = RedisStreamBroker(url=settings.redis.redis_url)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(
    schedule=[{
        "cron": settings.service.cron,
        "args": [],
        "kwargs": {},
        "cron_offset": None
    }]
)
async def scheduled_delete_expired_urls(
    service: ShortUrlService = TaskiqDepends(
        get_short_url_service_taskqi
    )
):
    await service.delete_expired_urls()

