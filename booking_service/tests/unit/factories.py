from polyfactory.factories.pydantic_factory import ModelFactory

from src.domain.entities.address import Address
from src.domain.entities.event import Event
from src.domain.entities.user import User


class UserFactory(ModelFactory[User]):
    __check_model__ = False


class AddressFactory(ModelFactory[Address]):
    __check_model__ = False


class EventFacroty(ModelFactory[Event]):
    __check_model__ = False
