from src.domain.entities import User
from src.domain.exceptions import UserIsExists
from src.domain.repositories import AbstractUserRepository


class FakeUserRepository(AbstractUserRepository):
    def __init__(self):
        self._users = {}

    async def create(self, email: str, password: str) -> User:
        if email in self._users:
            raise UserIsExists
        user = User(id="test-user-id", email=email, password=password, is_active=False)
        self._users[email] = user
        return user

    async def get_by_email(self, email: str) -> User | None:
        return self._users.get(email)

    async def get_by_id(self, user_id) -> User | None:
        return next((user for user in self._users.values() if user.id == user_id), None)

    async def update(self, user: User) -> User:
        self._users[user.email] = user
        return user
