import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.api.v1.schemas.event import EventCreateSchema, EventUpdateSchema
from src.core.config import settings
from src.infrastructure.db import postgres
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
        movie_id = uuid4()
        original_address_id = uuid4()
        updated_address_id = uuid4()

        print("\n===> STARTING EVENT REPOSITORY TEST")

        # === CREATE ===
        created_event = await repo.create(
            EventCreateSchema(
                movie_id=movie_id,
                address_id=original_address_id,
                owner_id=user_id,
                capacity=20,
                start_datetime=datetime.fromisoformat("2025-12-31T20:00:00+00:00").replace(tzinfo=None)
            )
        )
        assert created_event.id is not None
        assert created_event.movie_id == movie_id
        assert created_event.address_id == original_address_id
        print(f"[CREATE] Event created: {created_event}")

        # === GET BY ID ===
        fetched_event = await repo.get_by_id(created_event.id)
        assert fetched_event.id == created_event.id
        assert fetched_event.capacity == 20
        print(f"[GET BY ID] Event: {fetched_event}")

        # === UPDATE ===
        updated_event = await repo.update(
            created_event.id,
            EventUpdateSchema(
                address_id=updated_address_id,
                capacity=30
            )
        )
        assert updated_event.address_id == updated_address_id
        assert updated_event.capacity == 30
        print(f"[UPDATE] Updated Event: {updated_event}")

        # === GET EVENTS BY USER ID ===
        user_events = await repo.get_events_by_user_id(user_id)
        assert len(user_events) > 0
        assert any(e.id == created_event.id for e in user_events)
        print(f"[GET BY USER ID] Events for user {user_id}: {user_events}")

        # === GET EVENT LIST ===
        all_events = await repo.get_event_list(limit=10, offset=0)
        assert len(all_events) > 0
        assert any(e.id == created_event.id for e in all_events)
        print(f"[GET EVENT LIST] Events: {all_events}")

        # === DELETE ===
        delete_result = await repo.delete(created_event.id)
        assert delete_result is True
        print(f"[DELETE] Event with ID {created_event.id} deleted")

        # === CHECK DELETED ===
        try:
            await repo.get_by_id(created_event.id)
            assert False, "Event should not exist"
        except EventNotFoundError:
            print("[GET AFTER DELETE] Event not found (expected)")

        print("\n===> EVENT REPOSITORY TEST COMPLETE")

    await postgres.engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_event_repository())