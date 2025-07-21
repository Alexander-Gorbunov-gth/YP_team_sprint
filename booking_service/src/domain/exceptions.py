class NotEnoughSeatsError(Exception):
    """Недостаточно свободных мест в событии."""


class DuplicateReservationError(Exception):
    """Пользователь уже ранее бронировал (или пытался забронировать) это событие."""


class EventUpdateLockedError(Exception):
    """Событие нельзя отредактировать"""
