"""barcode.py

This module provides functions for parsing AAMVA (American Association of Motor Vehicle Administrators) barcode data.

Functions:
- header_length(version: int) -> int:
  Returns the length of the header based on the AAMVA version.

- remove_all_before(_str: str, indicator: str) -> str:
  Removes all characters in a string before a specified indicator.

- parse_file_header(file: str) -> dict:
  Parses the header of an AAMVA file and returns a dictionary with relevant information.

- parse_subfile_designator(file: str, aamva_version_number: int, designator_index: int) -> tuple:
  Parses the subfile designator from the file and returns a tuple with subfile type, offset, and length.

- parse_subfile(file: str, data_element_separator: str, segment_terminator: str, 
               subfile_type: str, offset: int, length: int) -> dict:
  Parses a subfile from the AAMVA file and returns a dictionary with its elements.

- parse_file(file: str) -> dict:
  Parses the entire AAMVA file and returns a dictionary containing the header and subfile information.

"""


def header_length(version: int) -> int:
    """
    Returns the length of the header based on the AAMVA version.

    Args:
        version (int): The AAMVA version number.

    Returns:
        int: The length of the header.
    """
    return 19 if version < 2 else 21


def remove_all_before(_str: str, indicator: str) -> str:
    """
    Removes all characters in a string before a specified indicator.

    Args:
        _str (str): The input string.
        indicator (str): The indicator to search for in the string.

    Returns:
        str: The modified string after removing characters before the indicator.

    Raises:
        ValueError: If the indicator is not found in the string.
    """
    if _str[0] != indicator:
        try:
            index = _str.index(indicator)
        except ValueError:
            raise ValueError(f"Indicator \"{indicator}\" is missing")
        _str = _str[index:]
    return _str


def parse_file_header(file: str) -> dict:
    """
    Parses the header of an AAMVA file and returns a dictionary with relevant information.

    Args:
        file (str): A string representing the content of the AAMVA file.

    Returns:
        dict: A dictionary containing the parsed header information.

    Raises:
        ValueError: If the file type in the header does not match the expected "ANSI ".
    """
    if file[4:9] != "ANSI ":
        raise ValueError(
            f"header file type missing \"{file[4:9]}\" != \"ANSI \"")
    header = dict(
        data_element_separator=str(file[1]),
        record_separator=str(file[2]),
        segment_terminator=str(file[3]),
        issuer_identification_number=int(file[9:15]),
        aamva_version_number=int(file[15:17])
    )
    if header["aamva_version_number"] < 2:
        header["jurisdiction_version_number"] = 0
        header["number_of_entries"] = int(file[17:19])
    else:
        header["jurisdiction_version_number"] = int(file[17:19])
        header["number_of_entries"] = int(file[19:21])
    return header


def parse_subfile_designator(
        file: str,
        aamva_version_number: int,
        designator_index: int) -> tuple:
    """
    Parses the subfile designator from the AAMVA file.

    Args:
        file (str): A string representing the content of the AAMVA file.
        aamva_version_number (int): The AAMVA version number.
        designator_index (int): The index of the subfile designator.

    Returns:
        tuple: A tuple containing subfile type, offset, and length.

    Raises:
        IndexError: If the calculated cursor position is out of range.
    """
    DESIGNATOR_LEGNTH = 10
    cursor = designator_index * DESIGNATOR_LEGNTH + \
        header_length(aamva_version_number)
    return (
        str(file[cursor:cursor + 2]),
        int(file[cursor + 2:cursor + 6]),
        int(file[cursor + 6:cursor + 10]))


def parse_subfile(
        file: str,
        data_element_separator: str,
        segment_terminator: str,
        subfile_type: str,
        offset: int,
        length: int) -> dict:
    """
    Parses a subfile from the AAMVA file and returns a dictionary with its elements.

    Args:
        file (str): A string representing the content of the AAMVA file.
        data_element_separator (str): The separator between data elements in the subfile.
        segment_terminator (str): The terminator for the subfile segment.
        subfile_type (str): The expected type of the subfile.
        offset (int): The starting position of the subfile in the file string.
        length (int): The length of the subfile in the file string.

    Returns:
        dict: A dictionary containing the parsed subfile information.

    Raises:
        ValueError: If the subfile type or segment terminator is not found in the specified positions.
    """
    end_offset = offset + length - 1
    if file[offset:offset + 2] != subfile_type:
        raise ValueError(
            f"Subfile is missing subfile type {ascii(file[offset:offset + 2])}\
                != {ascii(subfile_type)}")
    elif file[end_offset] != segment_terminator:
        raise ValueError(
            f"Subfile is missing segment terminator {ascii(file[end_offset])} \
                != {ascii(segment_terminator)}")
    subfile = {}
    elements = filter(
        None, file[offset + 2:end_offset].split(data_element_separator))
    for item in elements:
        subfile[item[:3]] = item[3:]
    return subfile


def parse_file(file: str) -> dict:
    """
    Parses the entire AAMVA file and returns a dictionary containing the header and subfile information.

    Args:
        file (str): A string representing the content of the AAMVA file.

    Returns:
        dict: A dictionary with "header" and "subfiles" keys, containing the parsed information.

    Raises:
        ValueError: If the number of entries in the header is less than 1.
    """
    file = remove_all_before(file, "@")
    header = parse_file_header(file)
    if header["number_of_entries"] < 1:
        raise ValueError("number of entries cannot be less than 1")
    subfiles = {}
    for i in range(header["number_of_entries"]):
        designator = parse_subfile_designator(
            file, header["aamva_version_number"], i)
        subfiles[designator[0]] = parse_subfile(
            file,
            header["data_element_separator"],
            header["segment_terminator"],
            *designator)
    return {
        "header": header,
        "subfiles": subfiles
    }
