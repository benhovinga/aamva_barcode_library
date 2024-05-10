from __future__ import annotations
from typing import NamedTuple, Optional

from errors import InvalidHeaderError


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
            file (str): Output from a barcode scanner.

        Returns:
            FileHeader: The file header object.

        Raises:
            IndexError: If the header length is too short.
            InvalidHeaderError: If a header element contains invalid data.
        """
        MIN_LENGTH = 17
        
        # Validation
        if len(file) < MIN_LENGTH:
            raise IndexError("Header length is too short.")
        elif file[0] != cls.COMPLIANCE_INDICATOR:
            raise InvalidHeaderError("COMPLIANCE_INDICATOR")
        elif file[1] != cls.DATA_ELEMENT_SEPARATOR:
            raise InvalidHeaderError("DATA_ELEMENT_SEPARATOR")
        elif file[2] != cls.RECORD_SEPARATOR:
            raise InvalidHeaderError("RECORD_SEPARATOR")
        elif file[3] != cls.SEGMENT_TERMINATOR:
            raise InvalidHeaderError("SEGMENT_TERMINATOR")
        elif file[4:9] != cls.FILE_TYPE:
            raise InvalidHeaderError("FILE_TYPE")
        
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
