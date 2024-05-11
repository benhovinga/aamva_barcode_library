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
from .FileHeader import FileHeader
from .SubfileDesignator import SubfileDesignator
from .Subfile import Subfile

from .utils import trim_before


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
    file = trim_before(FileHeader.COMPLIANCE_INDICATOR, file)
    header = FileHeader.parse(file)
    if header.number_of_entries < 1:
        raise ValueError("number of entries cannot be less than 1")
    
    subfiles = list()
    for i in range(header.number_of_entries):
        designator = SubfileDesignator.parse(
            file=file,
            aamva_version=header.aamva_version,
            designator_index=i)
        
        subfiles.append(Subfile.parse(file, designator))
    return {
        "header": header,
        "subfiles": subfiles
    }
