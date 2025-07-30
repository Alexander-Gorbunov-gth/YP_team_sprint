import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.api.v1.schemas.event import EventCreateSchema, EventUpdateSchema
from src.core.config import settings
from src.infrastructure.db import postgres
from src.domain.entities.event import Event
from src.infrastructure.repositories.events import SQLAlchemyEventRepository
from src.infrastructure.repositories.exceptions import EventNotFoundError


async def test_event_repository():
    # === 1. Инициализация движка и сессии ===
    postgres.engine = create_async_engine(settings.postgres.connection_url)
    postgres.session_maker = async_sessionmaker(
        bind=postgres.engine, expire_on_commit=False
    )

    # === 2. Получаем сессию через async генератор ===
    async with postgres.get_session() as session:

        repo = SQLAlchemyEventRepository(session)

        user_id = uuid4()

        print("\n===> STARTING EVENT REPOSITORY TEST")

        # === CREATE ===
        created_event = await repo.create(
            EventCreateSchema(
                movie_id=uuid4(),
                address_id="7858c0c6-0c1b-456a-99d4-948293ec4da9",
                owner_id=user_id,
                capacity=20,
                start_datetime=datetime.fromisoformat("2025-12-31T20:00:00+00:00").replace(tzinfo=None)
            )
        )
        print(f"[CREATE] Event created: {created_event}")

        # === GET BY ID ===
        fetched_event = await repo.get_by_id(created_event.id)
        print(f"[GET BY ID] Event: {fetched_event}")

        # === UPDATE ===
        updated_event = await repo.update(
            created_event.id,
            EventUpdateSchema(
                address_id=uuid4()
            )
        )
        print(f"[UPDATE] Updated Event: {updated_event}")

        # === GET EVENTS BY USER ID ===
        user_events = await repo.get_events_by_user_id(user_id)
        print(f"[GET BY USER ID] Events for user {user_id}: {user_events}")

        # === GET EVENT LIST ===
        all_events = await repo.get_event_list(limit=10, offset=0)
        print(f"[GET EVENT LIST] Events: {all_events}")

        # === DELETE ===
        await repo.delete(created_event.id)
        print(f"[DELETE] Event with ID {created_event.id} deleted")

        # === CHECK DELETED ===
        try:
            deleted_check = await repo.get_by_id(created_event.id)
            print(f"[GET AFTER DELETE] Event: {deleted_check}")
        except EventNotFoundError:
            print("[GET AFTER DELETE] Event not found")

        print("\n===> EVENT REPOSITORY TEST COMPLETE")

    await postgres.engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_event_repository())
