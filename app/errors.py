class ForbidenError(Exception):
    pass


class ResourceExistsError(Exception):
    pass


class ResourceDoesNotExistError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UnknownException(Exception):
    # Here is a lazy exception.
    pass


class TokenError(Exception):
    pass


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv
