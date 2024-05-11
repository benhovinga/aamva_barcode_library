from __future__ import annotations
from typing import NamedTuple

from .SubfileDesignator import SubfileDesignator
from .FileHeader import FileHeader

class Subfile(NamedTuple):
    subfile_type: str
    elements: dict
    
    @classmethod
    def parse(cls, file: str, designator: SubfileDesignator) -> Subfile:
        subfile_type = designator.subfile_type
        offset = designator.offset
        length = designator.length
        end_offset = offset + length - 1
        
        if file[offset:offset + 2] != subfile_type:
            raise ValueError("Subfile is missing subfile type.")
        elif file[end_offset] != FileHeader.SEGMENT_TERMINATOR:
            raise ValueError("Subfile is missing segment terminator.")
        
        items = filter(None, file[offset + 2: end_offset].split(FileHeader.DATA_ELEMENT_SEPARATOR))
        
        elements = dict()
        for item in items:
            elements[item[:3]] = item[3:]
        
        return cls(
            subfile_type=subfile_type,
            elements=elements
        )
