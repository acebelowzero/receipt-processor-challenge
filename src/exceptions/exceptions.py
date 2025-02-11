from http import HTTPStatus


class BaseException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str = "Base Exception"):
        super().__init__(self.message)


class HTTP400BadRequestError(BaseException):
    """Error 400."""

    status_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description

    def __init__(self, message=HTTPStatus.BAD_REQUEST.description):
        super().__init__(message)


class HTTP404NotFoundError(BaseException):
    """Error 404."""

    status_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description

    def __init__(self, message=HTTPStatus.NOT_FOUND.description):
        self.message = message
        super().__init__(self.message)
