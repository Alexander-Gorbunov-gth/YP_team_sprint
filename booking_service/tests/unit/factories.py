from polyfactory.factories.pydantic_factory import ModelFactory

from src.domain.dtos.address import AddressCreateDTO, AddressUpdateDTO
from src.domain.dtos.subscription import SubscriptionBaseDTO, SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.domain.entities.address import Address
from src.domain.entities.event import Event
from src.domain.entities.subscription import Subscription
from src.domain.entities.user import User


class UserFactory(ModelFactory[User]):
    __check_model__ = False


class AddressFactory(ModelFactory[Address]):
    __check_model__ = False


class EventFactory(ModelFactory[Event]):
    __check_model__ = False


class SubscriptionFactory(ModelFactory[Subscription]):
    __check_model__ = False


class SubscriptionDTOFactory(ModelFactory[SubscriptionBaseDTO]):
    __check_model__ = False


class SubscriptionCreateDTOFactory(ModelFactory[SubscriptionCreateDTO]):
    __check_model__ = False


class SubscriptionDeleteDTOFactory(ModelFactory[SubscriptionDeleteDTO]):
    __check_model__ = False


class AddressCreateDTOFactory(ModelFactory[AddressCreateDTO]):
    __check_model__ = False


class AddressUpdateDTOFactory(ModelFactory[AddressUpdateDTO]):
    __check_model__ = False
