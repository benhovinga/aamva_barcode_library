from typing import NamedTuple, Iterable, Optional, Literal

type BarcodeStr = str


class FileHeader(NamedTuple):
    issuer_id: int
    aamva_version: int
    number_of_entries: int
    jurisdiction_version: Optional[int] = 0


class SubfileDesignator(NamedTuple):
    subfile_type: str
    offset: int
    length: int


class Subfile(NamedTuple):
    subfile_type: str
    elements: dict[str, str]


class BarcodeFile(NamedTuple):
    header: FileHeader
    subfiles: Iterable[Subfile]


COMPLIANCE_INDICATOR = "@"
DATA_ELEMENT_SEPARATOR = "\n"
RECORD_SEPARATOR = "\x1e"
SEGMENT_TERMINATOR = "\r"
FILE_TYPE = "ANSI "


def trim_before(char: str, string: str) -> str:
    try:
        return string[string.index(char):]
    except ValueError:
        return string


def header_length(aamva_version: int) -> Literal[19, 21]:
    if aamva_version < 1 or aamva_version > 99:
        raise ValueError("aamva_version is out of range (1-99).")
    return 19 if aamva_version < 2 else 21


def parse_file_header(barcode_string: BarcodeStr) -> FileHeader:
    MIN_LENGTH = 17

    if len(barcode_string) < MIN_LENGTH:
        raise ValueError("Header length is too short.")
    elif barcode_string[0] != COMPLIANCE_INDICATOR:
        raise ValueError("Header element 'COMPLIANCE_INDICATOR' is invalid.")
    elif barcode_string[1] != DATA_ELEMENT_SEPARATOR:
        raise ValueError("Header element 'DATA_ELEMENT_SEPARATOR' is invalid.")
    elif barcode_string[2] != RECORD_SEPARATOR:
        raise ValueError("Header element 'RECORD_SEPARATOR' is invalid.")
    elif barcode_string[3] != SEGMENT_TERMINATOR:
        raise ValueError("Header element 'SEGMENT_TERMINATOR' is invalid.")
    elif barcode_string[4:9] != FILE_TYPE:
        raise ValueError("Header element 'FILE_TYPE' is invalid.")
    
    aamva_version = int(barcode_string[15:17])
    if len(barcode_string) < header_length(aamva_version):
        raise ValueError("Header length is too short.")
    
    issuer_id = int(barcode_string[9:15])
    number_of_entries = int(barcode_string[17:19] if aamva_version < 2 else barcode_string[19:21])
    jurisdiction_version = 0 if aamva_version < 2 else int(barcode_string[17:19])
    
    return FileHeader(
        issuer_id=issuer_id,
        aamva_version=aamva_version,
        number_of_entries=number_of_entries,
        jurisdiction_version=jurisdiction_version)


def parse_subfile_designator(barcode_string: BarcodeStr, aamva_version: int, designator_index: int) -> SubfileDesignator:
    DESIGNATOR_LENGTH = 10
    cursor = designator_index * DESIGNATOR_LENGTH + header_length(aamva_version)
    
    if len(barcode_string) < cursor + DESIGNATOR_LENGTH:
        raise ValueError("Subfile designator is too short.")
    
    return SubfileDesignator(
        subfile_type=str(barcode_string[cursor:cursor + 2]),
        offset=int(barcode_string[cursor + 2:cursor + 6]),
        length=int(barcode_string[cursor + 6:cursor + 10]))


def parse_subfile(barcode_string: BarcodeStr, designator: SubfileDesignator) -> Subfile:
    if type(designator) == tuple:
        designator = SubfileDesignator(*designator)
    subfile_type = designator.subfile_type
    offset = designator.offset
    length = designator.length
    end_offset = offset + length
    
    if len(barcode_string) < end_offset:
        raise ValueError("Subfile length is too short.")
    elif barcode_string[offset:offset + 2] != subfile_type:
        raise ValueError("Subfile is missing subfile type.")
    elif barcode_string[end_offset - 1] != SEGMENT_TERMINATOR:
        raise ValueError("Subfile is missing segment terminator.")
    
    items = filter(None, barcode_string[offset + 2: end_offset - 1].split(DATA_ELEMENT_SEPARATOR))
    elements = dict()
    for item in items:
        elements[item[:3]] = item[3:]
    
    return Subfile(
        subfile_type=subfile_type,
        elements=elements)


def parse_barcode_string(barcode_string: BarcodeStr) -> BarcodeFile:
    barcode_string = trim_before(COMPLIANCE_INDICATOR, barcode_string)
    header = parse_file_header(barcode_string)
    if header.number_of_entries < 1:
        raise ValueError("Number of entries cannot be less than 1.")
    
    subfiles = list()
    for i in range(header.number_of_entries):
        designator = parse_subfile_designator(barcode_string, header.aamva_version, i)
        subfile = parse_subfile(barcode_string, designator)
        subfiles.append(subfile)
    
    return BarcodeFile(
        header=header,
        subfiles=tuple(subfiles))
