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
    def from_str(cls, entry_num: int, _str: str) -> Self:
            start = entry_num * _DESIGNATOR_LENGTH + _HEADER_LENGTH
            return cls(
                subfile_type=   str(_str[start:start+2]),
                offset=         int(_str[start+2:start+6]),
                length=         int(_str[start+6:start+10]))
    
    def to_str(self) -> str:
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
    def from_str(cls, _str: str) -> Self:
        if len(_str) < _HEADER_LENGTH:
            raise Exception('Header too short')
        elif _str[0] != _COMPLIANCE_INDICATOR:
            raise Exception('Missing compliance indicator')
        elif _str[4:9] != 'ANSI ':
            raise Exception('Invalid or missing file type')
        return cls(
            compliance_indicator=           str(_str[0]),
            data_element_separator=         str(_str[1]),
            record_separator=               str(_str[2]),
            segment_terminator=             str(_str[3]),
            file_type=                      str(_str[4:9]),
            issuer_identification_number=   int(_str[9:15]),
            aamva_version_number=           int(_str[15:17]),
            jurisdiction_version_number=    int(_str[17:19]),
            number_of_entries=              int(_str[19:21]))
        
    def to_str(self) -> str:
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


class SubfileElement:
    code: str
    value: str
    
    def __init__(self, *args: str) -> None:
        """Create a SubfileElement object
        
        __init__(_str: str)
        __init__(code: str, value: str)
        """
        if args:
            if len(args) == 1:
                self.code, self.value = args[0][:3], args[0][3:]
            elif len(args) == 2:
                self.code, self.value = args[0], args[1]
        else:
            raise IndexError("arguments out of range")
    
    def __str__(self) -> str:
        return self.code + self.value
    
    def __repr__(self) -> str:
        return(f"SubfileElement(code={self.code}, value={self.value})")


@dataclass
class Subfile:
    subfile_type: str
    elements: list[SubfileElement]
    
    @classmethod
    def from_str(cls, header: FileHeader, subfile_designator: SubfileDesignator, _str: str) -> Self:
        start = subfile_designator.offset
        end = subfile_designator.offset + subfile_designator.length
        if _str[start:start + 2] != subfile_designator.subfile_type:
            raise Exception('Subfile and designator are not the same type')
        elif _str[end] != header.segment_terminator:
            raise Exception('Subfile missing segment terminator')
        return cls(
            subfile_designator.subfile_type,
            list(map(
                lambda i: SubfileElement(i),
                filter(None,map(
                    lambda i: i.strip(),
                    _str[start + 2: end].split(header.data_element_separator))))))
    
    def to_str(self, header: FileHeader) -> str:
        return str(
            self.subfile_type +
            header.data_element_separator.join(map(
                lambda i: str(i),
                self.elements)) +
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
    def from_str(cls, _str: str) -> Self:
        blob = cls.trim_to_indicator(_str, _COMPLIANCE_INDICATOR)
        header = FileHeader.from_str(blob)
        for i in range(header.number_of_entries):
            header.subfile_designators.append(SubfileDesignator.from_str(i, blob))
        subfiles = []
        for subfile_designator in header.subfile_designators:
            subfiles.append(Subfile.from_str(header, subfile_designator, blob))
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
    
    def to_str(self) -> str:
        subfiles = tuple(map(
            lambda subfile: subfile.to_str(self.header),
            self.subfiles))
        self.header.number_of_entries = len(subfiles)
        self.header.subfile_designators = self.create_subfile_designators(subfiles)
        subfile_designators = tuple(map(
            lambda designator: designator.to_str(),
            self.header.subfile_designators))
        return str(self.header.to_str() + "".join(subfile_designators) + "".join(subfiles))
