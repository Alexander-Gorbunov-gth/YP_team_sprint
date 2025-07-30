class EventTimeConflictError(Exception):
    pass


class EventNotFoundError(Exception):
    pass


class ReservationNotFoundError(Exception):
    pass


class SessionHasExpired(Exception):
    """Исключение, которое выбрасывается, если сессия истекла."""
