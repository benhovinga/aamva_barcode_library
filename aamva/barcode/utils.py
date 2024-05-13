def trim_before(char: str, string: str) -> str:
    """
    Removes everything before 'char' in 'string'.

    Args:
        char (str): A character to search for in the string.
        string (str): The string to trim.

    Returns:
        str: The trimmed string.
    """
    if string[0] != char:
        index = string.index(char)
        string = string[index:]
    return string
