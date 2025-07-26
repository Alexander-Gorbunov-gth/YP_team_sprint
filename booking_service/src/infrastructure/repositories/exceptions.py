class SubscriptionAlreadyExistsError(Exception):
    """Исключение, которое вызывается, когда попытка создать подписку, которая уже существует."""


class SubscriptionNotFoundError(Exception):
    """Исключение, которое вызывается, когда попытка удалить подписку, которая не существует."""
