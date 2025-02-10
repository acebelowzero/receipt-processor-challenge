from src.exceptions.base_exceptions import BaseException


class ElementNotFoundError(BaseException):
    """Raised when an element is not found in the database."""


class DatabaseConnectionError(BaseException):
    """Raised when a database connection error occurs."""