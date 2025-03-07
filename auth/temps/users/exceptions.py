class RepositoryError(Exception):
    """Базовый класс для всех ошибок репозитория"""

    def __init__(self, message: str):
        self.message = message


class EntityAlreadyExistsError(RepositoryError):
    """Возникает при попытке создать сущность, которая уже существует"""

    pass


class EntityNotFoundError(RepositoryError):
    """Возникает когда сущность не найдена"""

    pass


class PermissionAssociationError(RepositoryError):
    """Возникает при проблемах с привязкой разрешений"""

    pass
