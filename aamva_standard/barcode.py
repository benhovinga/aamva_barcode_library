"""
The barcode module parses identification card barcode data into python objects
"""


def header_length(version: int) -> int:
    """
    Returns the header length for the given version
    
    In version 2 of the AAMVA ID/DL standards a 2 byte jurisdiction version was
    added to the header of the file. This change increased the total size of
    the header from 19 bytes to 21 bytes.
    """
    return 19 if version < 2 else 21


def remove_all_before(_str: str, indicator: str) -> str:
    """
    Removes all characters before the indicator in a string
    
    Example:
    
    remove_all_before("abc@123", "@")
    returns: "@123"
    
    Raises a ValueError if the indicator is not found in the string.
    """
    if _str[0] != indicator:
        try:
            index = _str.index(indicator)
        except ValueError:
            raise ValueError(f"Indicator \"{indicator}\" is missing")
        _str = _str[index:]
    return _str


def parse_file_header(file: str) -> dict:
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
