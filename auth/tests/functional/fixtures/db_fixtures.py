import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.postgres import start_mappers
from src.models.adapters.orm import metadata
from tests.functional.settings import test_settings


class TestDatabase:
    def __init__(self, settings):
        self.engine = create_async_engine(
            settings.db.db_url, echo=settings.db.postgres_echo
        )
        self.SessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
        start_mappers()

    async def drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def clean_tables(self):
        async with self.engine.begin() as conn:
            for table in reversed(metadata.sorted_tables):
                if table.name == "users":
                    await conn.execute(
                        text("DELETE FROM users WHERE email LIKE 'test_%@gmail.com'")
                    )
                else:
                    await conn.execute(table.delete())

    async def get_session(self):
        async with self.SessionLocal() as session:
            yield session


pytest_db = TestDatabase(settings=test_settings)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    await pytest_db.create_db()
    yield
    await pytest_db.drop_db()


@pytest_asyncio.fixture(autouse=True)
async def clean_table():
    yield
    await pytest_db.clean_tables()


@pytest_asyncio.fixture
async def client_session():
    async for session in pytest_db.get_session():
        yield session
