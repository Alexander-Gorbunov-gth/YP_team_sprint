from polyfactory.factories.pydantic_factory import ModelFactory

from src.domain.entities.address import Address
from src.domain.entities.event import Event
from src.domain.entities.user import User
from src.api.v1.schemas.event import EventCreateSchema, EventUpdateSchema


class UserFactory(ModelFactory[User]):
    __check_model__ = False


class AddressFactory(ModelFactory[Address]):
    __check_model__ = False


class EventFacroty(ModelFactory[Event]):
    __check_model__ = False


class EventCreateFactory(ModelFactory[EventCreateSchema]):
    __check_model__ = False


class EventUpdateFactory(ModelFactory[EventUpdateSchema]):
    __check_model__ = False
