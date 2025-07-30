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
