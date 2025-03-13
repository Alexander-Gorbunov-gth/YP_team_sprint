class UserIsExists(Exception):
    pass


class WrongEmailOrPassword(Exception):
    pass


class WrongOldPassword(Exception):
    pass


class PasswordsNotMatch(Exception):
    pass


class Forbidden(Exception):
    pass


class NotAuthorized(Exception):
    pass
