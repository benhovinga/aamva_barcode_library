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
    "number_of_entries",
])

SubfileDesignator = namedtuple("SubfileDesignator", [
    "type",
    "offset",
    "legth",
])

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

def read_subfile_designators(file: str, file_header: FileHeader) -> tuple[SubfileDesignator]:
    if file_header == 0:
        raise ValueError("file has not subfiles")
    designators = []
    for i in range(file_header.number_of_entries):
        cursor = i * DESIGNATOR_LENGTH + HEADER_LENGTH
        designators.append(SubfileDesignator(
            type=   str(file[cursor:cursor + 2]),
            offset= int(file[cursor + 2:cursor + 6]),
            legth=  int(file[cursor + 6:cursor + 10]),
        ))
    return tuple(designators)
