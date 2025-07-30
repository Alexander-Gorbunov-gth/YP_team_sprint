class SubscriptionAlreadyExistsError(Exception):
    """Исключение, которое вызывается, когда попытка создать подписку, которая уже существует."""


class SubscriptionNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить подписку, которая не существует."""


class EventNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить событие, которая не существует."""


class ReservationNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить бронь, которая не существует."""
