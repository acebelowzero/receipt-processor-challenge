from src.exceptions import exceptions


class ElementNotFoundError(exceptions.BaseException):
    """Raised when an element is not found in the database."""

    def __init__(self, message: str = "Element cannot be found"):
        self.message = message
        super().__init__(message=self.message)


class DatabaseConnectionError(exceptions.BaseException):
    """Raised when a database connection error occurs."""
