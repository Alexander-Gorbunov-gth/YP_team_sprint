from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from src.core.config import settings



Base = declarative_base()

engine = create_async_engine(settings.db.db_url, echo=True, future=True)


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def create_database() -> None:
    from src.models.users import User
    from src.models.permissions import Permission
    from src.models.sessions import Session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    from src.models.permissions import Permission
    from src.models.users import User
    from src.models.sessions import Session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
