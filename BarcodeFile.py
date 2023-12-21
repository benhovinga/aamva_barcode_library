from dataclasses import dataclass, field
from typing import Self

_HEADER_LENGTH = 21
_DESIGNATOR_LENGTH = 10
_COMPLIANCE_INDICATOR = "@"


@dataclass
class SubfileDesignator:
    subfile_type: str
    offset: int
    length: int
    
    @classmethod
    def decode(cls, entry_num: int, blob: str) -> Self:
            start = entry_num * _DESIGNATOR_LENGTH + _HEADER_LENGTH
            return cls(
                subfile_type=   str(blob[start:start+2]),
                offset=         int(blob[start+2:start+6]),
                length=         int(blob[start+6:start+10]))
    
    def encode(self) -> str:
        return str(
            self.subfile_type +
            str(self.offset).rjust(4, "0") +
            str(self.length).rjust(4, "0"))


@dataclass
class FileHeader:
    compliance_indicator: str = "@"
    data_element_separator: str = "\n"
    record_separator: str = ""
    segment_terminator: str = "\r"
    file_type: str = "ANSI "
    issuer_identification_number: int = 0
    aamva_version_number: int = 10
    jurisdiction_version_number: int = 0
    number_of_entries: int = 0
    subfile_designators: list[SubfileDesignator] = field(default_factory=list)
    
    @classmethod
    def decode(cls, blob: str) -> Self:
        if len(blob) < _HEADER_LENGTH:
            raise Exception('Header too short')
        elif blob[0] != _COMPLIANCE_INDICATOR:
            raise Exception('Missing compliance indicator')
        elif blob[4:9] != 'ANSI ':
            raise Exception('Invalid or missing file type')
        return cls(
            compliance_indicator=           str(blob[0]),
            data_element_separator=         str(blob[1]),
            record_separator=               str(blob[2]),
            segment_terminator=             str(blob[3]),
            file_type=                      str(blob[4:9]),
            issuer_identification_number=   int(blob[9:15]),
            aamva_version_number=           int(blob[15:17]),
            jurisdiction_version_number=    int(blob[17:19]),
            number_of_entries=              int(blob[19:21]))
        
    def encode(self) -> str:
        return str(
            self.compliance_indicator +
            self.data_element_separator +
            self.record_separator +
            self.segment_terminator +
            self.file_type +
            str(self.issuer_identification_number).rjust(6, "0") +
            str(self.aamva_version_number).rjust(2, "0") +
            str(self.jurisdiction_version_number).rjust(2, "0") +
            str(self.number_of_entries).rjust(2, "0"))


@dataclass
class Subfile:
    subfile_type: str
    elements: list[str]
    
    @classmethod
    def decode(cls, header: FileHeader, subfile_designator: SubfileDesignator, blob: str) -> Self:
        start = subfile_designator.offset
        end = subfile_designator.offset + subfile_designator.length
        if blob[start:start + 2] != subfile_designator.subfile_type:
            raise Exception('Subfile and designator are not the same type')
        elif blob[end] != header.segment_terminator:
            raise Exception('Subfile missing segment terminator')
        return cls(
            subfile_designator.subfile_type,
            list(filter(None,map(
                lambda i: i.strip(),
                blob[start + 2: end].split(header.data_element_separator)))))
    
    def encode(self, header: FileHeader) -> str:
        return str(
            self.subfile_type +
            header.data_element_separator.join(self.elements) +
            header.segment_terminator)


@dataclass
class BarcodeFile:
    header: FileHeader
    subfiles: list[Subfile]
    
    @staticmethod
    def trim_to_indicator(_str: str, indicator: str) -> str:
        """Remove everything before the indicator"""
        if _str[0] != indicator:
            try:
                index = _str.index(indicator)
            except ValueError:
                raise ValueError(f"Indicator \"{indicator}\" is missing")
            _str = _str[index:]
        return _str

    @classmethod
    def decode(cls, _str: str) -> Self:
        blob = cls.trim_to_indicator(_str, _COMPLIANCE_INDICATOR)
        header = FileHeader.decode(blob)
        for i in range(header.number_of_entries):
            header.subfile_designators.append(SubfileDesignator.decode(i, blob))
        subfiles = []
        for subfile_designator in header.subfile_designators:
            subfiles.append(Subfile.decode(header, subfile_designator, blob))
        return cls(header, subfiles)
    
    @staticmethod
    def create_subfile_designators(subfiles: tuple[str]) -> tuple[SubfileDesignator]:
        subfile_designators = []
        subfile_designator_length = len(subfiles) + _DESIGNATOR_LENGTH
        next_offset = 0
        for i in range(len(subfiles)):
            offset = _HEADER_LENGTH + subfile_designator_length + next_offset
            next_offset = offset + len(subfiles[i]) + 1
            subfile_designators.append(SubfileDesignator(subfiles[i][:2], offset, len(subfiles[i])))
        return tuple(subfile_designators)
    
    def encode(self) -> str:
        subfiles = tuple(map(
            lambda subfile: subfile.encode(self.header),
            self.subfiles))
        self.header.number_of_entries = len(subfiles)
        self.header.subfile_designators = self.create_subfile_designators(subfiles)
        subfile_designators = tuple(map(
            lambda designator: designator.encode(),
            self.header.subfile_designators))
        return str(self.header.encode() + "".join(subfile_designators) + "".join(subfiles))
