import asyncio
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.db import postgres
from src.infrastructure.repositories.subscriptions import SQLAlchemySubscriptionRepository


async def test_repository():
    # === 1. Инициализируем engine и сессию ===
    postgres.engine = create_async_engine(settings.postgres.connection_url)
    postgres.async_session_maker = async_sessionmaker(bind=postgres.engine, expire_on_commit=False)

    # === 2. Получаем сессию через async генератор get_session ===
    session_gen = postgres.get_session()
    session = await anext(session_gen)

    repo = SQLAlchemySubscriptionRepository(session)

    user_id = uuid4()
    host_id = uuid4()

    print(f"\n===> STARTING TEST with user_id={user_id}, host_id={host_id}")

    created = await repo.create(host_id=host_id, user_id=user_id)
    print(f"[CREATE] Subscription created: {created}")

    duplicate = await repo.create(host_id=host_id, user_id=user_id)
    print(f"[DUPLICATE CHECK] Subscription returned: {duplicate}")

    subscriptions = await repo.get_subscriptions_by_user_id(user_id=user_id)
    print(f"[GET] Subscriptions for user_id: {subscriptions}")

    deleted = await repo.delete(host_id=host_id, user_id=user_id)
    print(f"[DELETE] Subscription deleted: {deleted}")

    after_delete = await repo.get_subscriptions_by_user_id(user_id=user_id)
    print(f"[GET AFTER DELETE] Subscriptions for user_id: {after_delete}")

    print("\n===> TEST COMPLETE")

    # Завершаем генератор и закрываем engine
    await session_gen.aclose()
    await postgres.engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_repository())
