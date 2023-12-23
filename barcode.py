from collections import namedtuple

HEADER_LENGTH = 21
COMPLIANCE_INDICATOR = "@"
DESIGNATOR_LENGTH = 10

FileHeader = namedtuple("FileHeader", [
    "compliance_indicator",
    "data_element_separator",
    "record_separator",
    "segment_terminator",
    "file_type",
    "issuer_identification_number",
    "aamva_version_number",
    "jurisdiction_version_number",
    "number_of_entries"])

SubfileDesignator = namedtuple("SubfileDesignator", [
    "type",
    "offset",
    "legth"])

def trim_to_indicator(_str: str, indicator: str) -> str:
    """Remove everything before the indicator, moving the indicator to the begining of the string"""
    if _str[0] != indicator:
        try:
            index = _str.index(indicator)
        except ValueError:
            raise ValueError(f"Indicator \"{indicator}\" is missing")
        _str = _str[index:]
    return _str

def read_file_header(file: str) -> FileHeader:
    if len(file) < HEADER_LENGTH:
        raise ValueError("file too short")
    elif file[0] != COMPLIANCE_INDICATOR:
        file = trim_to_indicator(file, COMPLIANCE_INDICATOR)
    if file[4:9] != "ANSI ":
        raise ValueError("file missing file type")
    return FileHeader(
            compliance_indicator=           str(file[0]),
            data_element_separator=         str(file[1]),
            record_separator=               str(file[2]),
            segment_terminator=             str(file[3]),
            file_type=                      str(file[4:9]),
            issuer_identification_number=   int(file[9:15]),
            aamva_version_number=           int(file[15:17]),
            jurisdiction_version_number=    int(file[17:19]),
            number_of_entries=              int(file[19:21]))

def read_subfile_designator(file: str, designator_index: int) -> SubfileDesignator:
    cursor = designator_index * DESIGNATOR_LENGTH + HEADER_LENGTH
    return SubfileDesignator(
        type=   str(file[cursor:cursor + 2]),
        offset= int(file[cursor + 2:cursor + 6]),
        legth=  int(file[cursor + 6:cursor + 10]))

def read_subfile(file: str, segment_terminator: str, data_element_separator: str, subfile_type: str, offset: int, length: int) -> dict[str, str]:
    end_offset = offset + length
    if file[offset:offset + 2] != subfile_type:
        raise ValueError("found subfile and designator type are not the same")
    elif file[end_offset] != segment_terminator:
        raise ValueError("subfile is missing segment terminator")
    subfile = {"_type": subfile_type}
    elements = filter(None, file[offset + 2:end_offset].split(data_element_separator))
    for item in elements:
        subfile[item[:3]] = item[3:]
    return subfile
