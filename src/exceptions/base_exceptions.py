class BaseException(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str = "An error occurred."):
        self.message = message

    def __str__(self):
        return repr(self.message)