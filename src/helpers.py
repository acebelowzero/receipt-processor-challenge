"""
Global helper functions
"""

import re


def remove_nonalphanumeric_characters(string: str) -> str:
    """
    removes nonalphanumeric characters
    Args:
        string (str) - string to format

    Returns:
        cleaned string
    """
    if string:
        return re.sub(r"\W+", "", string)


def check_if_whole_number(amount: float):
    """
    check if
    """
    return amount % 1 == 0


def count_groups_of_two(items: list):
    """
    counts groups of two
    """
    # floor operation
    return len(items) // 2


def is_odd(num: int):
    """
    check if a  number is odd or even
    """
    if num % 2 == 0:
        return False
    return True
