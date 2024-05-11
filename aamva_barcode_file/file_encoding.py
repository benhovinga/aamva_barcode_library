from .file_header import FileHeader
from .subfile_designator import SubfileDesignator
from .subfile import Subfile

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
