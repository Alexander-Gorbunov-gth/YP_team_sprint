class EventTimeConflictError(Exception):
    pass


class EventNotFoundError(Exception):
    pass


class EventStartDatetimeError(Exception):
    """Исключение, которое выбрасывается, если дата начала события в прошлом."""


class EventNotOwnerError(Exception):
    """Исключение, которое выбрасывается, если пользователь не является владельцем события."""


class ReservationNotFoundError(Exception):
    pass


class SessionHasExpired(Exception):
    """Исключение, которое выбрасывается, если сессия истекла."""


class AddressNotFoundError(Exception):
    """Исключение, которое выбрасывается, если адрес не найден."""


class ForbiddenError(Exception):
    """Исключение, которое выбрасывается, если пользователь не имеет доступа к ресурсу."""


class SubscriptionAlreadyExistsError(Exception):
    """Исключение, которое вызывается, когда попытка создать подписку, которая уже существует."""


class SubscriptionNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить подписку, которая не существует."""
