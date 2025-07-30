class SubscriptionAlreadyExistsError(Exception):
    """Исключение, которое вызывается, когда попытка создать подписку, которая уже существует."""


class SubscriptionNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить подписку, которая не существует."""

    
class AddressNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка получить адрес, который не существует."""


class NotModifiedError(Exception):
    """Исключение, которое вызывается, когда не указаны данные для обновления."""
    

class EventNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить событие, которая не существует."""


class ReservationNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить бронь, которая не существует."""
