import asyncio
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.domain.dtos.address import AddressCreateDTO, AddressUpdateDTO
from src.infrastructure.db import postgres
from src.infrastructure.repositories.addresses import SQLAlchemyAddressRepository


async def test_repository():
    # === 1. Инициализируем engine и сессию ===
    postgres.engine = create_async_engine(settings.postgres.connection_url)
    postgres.async_session_maker = async_sessionmaker(
        bind=postgres.engine, expire_on_commit=False
    )

    # === 2. Получаем сессию через async генератор get_session ===
    session_gen = postgres.get_session()
    session = await anext(session_gen)

    repo = SQLAlchemyAddressRepository(session)

    user_id = uuid4()
    latitude = 55.7558
    longitude = 37.6173
    country = "Russia"
    city = "Moscow"
    street = "Tverskaya"
    house = "1"
    flat = "101"

    print("\n===> STARTING TEST")

    # Test create
    created = await repo.create(
        address=AddressCreateDTO(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            country=country,
            city=city,
            street=street,
            house=house,
            flat=flat,
        ),
    )
    assert created.id is not None
    assert created.user_id == user_id
    assert created.latitude == latitude
    assert created.longitude == longitude
    print(f"[CREATE] Address created: {created}")

    # Test get
    address = await repo.get_address(created.id)
    assert address.id == created.id
    assert address.country == country
    print(f"[GET] Addresses for user_id: {address}")

    # Test update
    updated = await repo.update(
        address=AddressUpdateDTO(
            country="Updated Country",
            city="Updated City",
            street="Updated Street",
            house="Updated House",
            flat="Updated Flat",
        ),
        address_id=created.id
    )
    assert updated.country == "Updated Country"
    assert updated.city == "Updated City"
    print(f"[UPDATE] Address updated: {updated}")

    # Test get_my_addresses
    my_addresses = await repo.get_my_address(user_id=user_id)
    assert len(my_addresses) == 1
    assert my_addresses[0].id == created.id
    print(f"[GET MY ADDRESSES] Addresses for user_id: {my_addresses}")

    # Test delete
    deleted = await repo.delete(address_id=created.id)
    assert deleted is True
    print(f"[DELETE] Address deleted: {deleted}")

    # Verify deletion
    after_delete = await repo.get_my_address(user_id=user_id)
    assert len(after_delete) == 0
    print(f"[GET AFTER DELETE] Address for user_id: {after_delete}")

    print("\n===> TEST COMPLETE")

    # Завершаем генератор и закрываем engine
    await session_gen.aclose()
    await postgres.engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_repository())