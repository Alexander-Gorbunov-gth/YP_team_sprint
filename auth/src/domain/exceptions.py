class UserIsExists(Exception):
    pass


class WrongEmailOrPassword(Exception):
    pass


class WrongOldPassword(Exception):
    pass


class PasswordsNotMatch(Exception):
    pass


class RoleIsExists(Exception):
    pass


class PermissionIsExists(Exception):
    pass


class RoleNotFound(Exception):
    pass


class PermissionNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass

class Forbidden(Exception):
    pass


class NotAuthorized(Exception):
    pass
