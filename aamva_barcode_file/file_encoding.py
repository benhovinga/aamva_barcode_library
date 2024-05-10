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
from FileHeader import FileHeader


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
        FileHeader.header_length(aamva_version_number)
    return (
        str(file[cursor:cursor + 2]),
        int(file[cursor + 2:cursor + 6]),
        int(file[cursor + 6:cursor + 10]))


def parse_subfile(
        file: str,
        subfile_type: str,
        offset: int,
        length: int) -> dict:
    """
    Parses a subfile from the AAMVA file and returns a dictionary with its elements.

    Args:
        file (str): A string representing the content of the AAMVA file.
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
    elif file[end_offset] != FileHeader.SEGMENT_TERMINATOR:
        raise ValueError(
            f"Subfile is missing segment terminator {ascii(file[end_offset])} \
                != {ascii(FileHeader.SEGMENT_TERMINATOR)}")
    subfile = {}
    elements = filter(
        None, file[offset + 2:end_offset].split(FileHeader.DATA_ELEMENT_SEPARATOR))
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
    header = FileHeader.parse(file)
    if header.number_of_entries < 1:
        raise ValueError("number of entries cannot be less than 1")
    subfiles = {}
    for i in range(header.number_of_entries):
        designator = parse_subfile_designator(
            file, header.aamva_version, i)
        subfiles[designator[0]] = parse_subfile(
            file, *designator)
    return {
        "header": header,
        "subfiles": subfiles
    }
