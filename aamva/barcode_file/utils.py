"""utils.py

This module provides functional tools for the project.
"""


def trim_before(char: str, _str: str) -> str:
    """
    Removes everything before the first instance of a character in a given string.

    Args:
        char (str): A character to search for in the string.
        _str (str): The string to modify.

    Returns:
        str: The modified string.

    Raises:
        TypeError: When char doesn't have a length of 1.
        ValueError: If char is not found in the string.
    """
    if type(char) != str or len(char) != 1:
        raise TypeError(f"char must have a length of 1")
    if _str[0] != char:
        try:
            index = _str.index(char)
        except ValueError:
            raise ValueError(f"Character \"{char}\" not found in string")
        _str = _str[index:]
    return _str
