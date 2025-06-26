from src.domain.clients import Client
from uuid import UUID

auth_client_mock_data = [
    Client(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        name="Mock User",
        email="mockuser@example.com",
        active_channels=["email", "push"],
        timezone="UTC",
    ),
    Client(
        id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        name="Mock User 2",
        email="mockuser2@example.com",
        active_channels=["email", "push"],
        timezone="Europe/Moscow",
    ),
    Client(
        id=UUID("123e4567-e89b-12d3-a456-426614174002"),
        name="Mock User 3",
        email="mockuser3@example.com",
        active_channels=["email", "push"],
        timezone="America/New_York",
    ),
]
