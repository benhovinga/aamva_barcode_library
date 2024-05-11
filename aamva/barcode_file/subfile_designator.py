from __future__ import annotations
from typing import NamedTuple

from .file_header import FileHeader


class SubfileDesignator(NamedTuple):
    subfile_type: str
    offset: int
    length: int
    
    @classmethod
    def parse(cls, file: str, aamva_version: int, designator_index: int) -> SubfileDesignator:
        DESIGNATOR_LENGTH = 10
        cursor = designator_index * DESIGNATOR_LENGTH + FileHeader.header_length(aamva_version)
        
        if len(file) < cursor + DESIGNATOR_LENGTH:
            raise IndexError("Subfile designator too short.")
        
        return cls(
            subfile_type=str(file[cursor:cursor + 2]),
            offset=int(file[cursor + 2:cursor + 6]),
            length=int(file[cursor + 6:cursor + 10])
        )
    
    def unparse(self):
        return self.subfile_type + \
            str(self.offset).rjust(4, "0") + \
            str(self.length).rjust(4, "0")
