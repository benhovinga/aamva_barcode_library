from __future__ import annotations
from typing import NamedTuple, Optional


class FileHeader(NamedTuple):
    """
    Represents the Header of a file that would be stored in a barcode
    """
    issuer_id: int
    aamva_version: int
    number_of_entries: int
    jurisdiction_version: Optional[int] = 0
    
    # Static header elements
    COMPLIANCE_INDICATOR = "@"
    DATA_ELEMENT_SEPARATOR = "\n"
    RECORD_SEPARATOR = "\x1e"
    SEGMENT_TERMINATOR = "\r"
    FILE_TYPE = "ANSI "
    
    @classmethod
    def parse(cls, file: str) -> FileHeader:
        """
        Parses the file header and returns a structured Header object.

        Args:
            file (str): A string representing the content of the AAMVA file.

        Returns:
            dict: A dictionary containing the parsed header information.

        Raises:
            ValueError: If header contains invalid data.
        """
        # Validation
        if file[0] != cls.COMPLIANCE_INDICATOR:
            raise ValueError("Compliance Indicator is invalid.")
        elif file[1] != cls.DATA_ELEMENT_SEPARATOR:
            raise ValueError("Data Element Separator is invalid.")
        elif file[2] != cls.RECORD_SEPARATOR:
            raise ValueError("Record Separator is invalid.")
        elif file[3] != cls.SEGMENT_TERMINATOR:
            raise ValueError("Segment Terminator is invalid.")
        elif file[4:9] != cls.FILE_TYPE:
            raise ValueError("File Type is invalid.")
        
        version = int(file[15:17])
        if version < 2:
            return cls(
                issuer_id=int(file[9:15]),
                aamva_version=version,
                number_of_entries=int(file[17:19])
            )
        
        return cls(
            issuer_id=int(file[9:15]),
            aamva_version=version,
            number_of_entries=int(file[19:21]),
            jurisdiction_version=int(file[17:19])
        )
    
    def unparse(self) -> str:
        """Converts the structured Header object into a file header string.

        Returns:
            str: file header
        """
        jurisdiction = str(self.jurisdiction_version).rjust(2, '0') if self.aamva_version > 1 else ""
        return self.COMPLIANCE_INDICATOR + \
            self.DATA_ELEMENT_SEPARATOR + \
            self.RECORD_SEPARATOR + \
            self.SEGMENT_TERMINATOR + \
            self.FILE_TYPE + \
            str(self.issuer_id).rjust(6, '0') + \
            str(self.aamva_version).rjust(2, '0') + \
            jurisdiction + \
            str(self.number_of_entries).rjust(2, '0')
