class EventTimeConflictError(Exception):
    pass


class EventNotFoundError(Exception):
    pass


class ReservationNotFoundError(Exception):
    pass


class SessionHasExpired(Exception):
    """Исключение, которое выбрасывается, если сессия истекла."""


class AddressNotFoundError(Exception):
    """Исключение, которое выбрасывается, если адрес не найден."""


class SubscriptionAlreadyExistsError(Exception):
    """Исключение, которое вызывается, когда попытка создать подписку, которая уже существует."""


class SubscriptionNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить подписку, которая не существует."""
