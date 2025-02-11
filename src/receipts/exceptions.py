from src.exceptions import exceptions

"""Exceptions for receipt service"""


class ReceiptServiceError(exceptions.BaseException):
    """Receipts service error exception"""

    message = "Recepit Service error"

    def __init__(self, message="Receipt Service Error"):
        self.message = message
        super().__init__(self.message)
