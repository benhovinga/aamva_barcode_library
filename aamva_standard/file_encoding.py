"""file_encoding.py

This module provides functions for parsing AAMVA DL/ID barcode data.

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
from utils import trim_before


# Static File Header Elements
COMPLIANCE_INDICATOR = "@"
DATA_ELEMENT_SEPARATOR = "\n"
RECORD_SEPARATOR = "\x1e"
SEGMENT_TERMINATOR = "\r"
FILE_TYPE = "ANSI "


def header_length(version: int) -> int:
    """
    Returns the length of the header based on the AAMVA version. In version 2
    of the AAMVA Standard the header length increased from 19 bytes to 21
    bytes. This is to accomidate a new 2 byte field called "jurisdiction
    version number" in the header.

    Args:
        version (int): The AAMVA version number.

    Returns:
        int: The length of the header (19 or 21)
    """
    return 19 if version < 2 else 21


def parse_file_header(file: str) -> dict:
    """
    Parses the header of an AAMVA file and returns a dictionary with relevant information.

    Args:
        file (str): A string representing the content of the AAMVA file.

    Returns:
        dict: A dictionary containing the parsed header information.

    Raises:
        ValueError: If header contains invalid data.
    """
    # Validate core header elements
    if file[0] != COMPLIANCE_INDICATOR:
        raise ValueError("Compliance Indicator is invalid.")
    elif file[1] != DATA_ELEMENT_SEPARATOR:
        raise ValueError("Data Element Separator is invalid.")
    elif file[2] != RECORD_SEPARATOR:
        raise ValueError("Record Separator is invalid.")
    elif file[3] != SEGMENT_TERMINATOR:
        raise ValueError("Segment Terminator is invalid.")
    elif file[4:9] != FILE_TYPE:
        raise ValueError("File Type is invalid.")
    
    header = dict()
    header["issuer_identification_number"] = int(file[9:15])
    header["aamva_version_number"] = int(file[15:17])
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
    file = trim_before("@", file)
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
