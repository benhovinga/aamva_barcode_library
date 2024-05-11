from __future__ import annotations
from typing import NamedTuple, Iterable

from .file_header import FileHeader
from .subfile_designator import SubfileDesignator
from .subfile import Subfile

from .utils import trim_before


class BarcodeFile(NamedTuple):
    header: FileHeader
    subfiles: Iterable[Subfile]
    
    @classmethod
    def parse(cls, file:str) -> BarcodeFile:
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
            subfile = Subfile.parse(file, designator)
            subfiles.append(subfile)
        
        return cls(
            header=header,
            subfiles=tuple(subfiles)
        )
