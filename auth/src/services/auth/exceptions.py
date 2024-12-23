class BaseUserError(Exception):
    pass


class UserIsExist(BaseUserError):
    pass


class BaseAuthException(Exception):
    pass


class UserNotFoundError(BaseAuthException):
    pass


class InvalidPasswordError(BaseAuthException):
    pass


class BaseSessionError(Exception):
    pass


class SessionHasExpired(BaseSessionError):
    pass


class AuthError(BaseSessionError):
    pass
