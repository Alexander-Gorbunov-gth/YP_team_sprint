from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import clear_mappers

from src.models.adapters.orm import metadata, start_mappers
from src.core.config import settings


engine = create_async_engine(settings.db.db_url, echo=True, future=True)


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()


async def purge_database() -> None:
    clear_mappers()
