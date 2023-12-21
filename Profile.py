from dataclasses import dataclass, field
from typing import Any, Self
from Enums import Card
from BarcodeFile import BarcodeFile
from ElementField import ElementField

from example_data import barcode0
    

@dataclass
class Profile:
    _issuer_identification_number: int
    _aamva_version_number: int
    _jurisdiction_version_number: int
    profile_type: Card
    mandatory_fields: dict[ElementField, Any]
    optional_fields: dict[ElementField, Any]
    
    @classmethod
    def from_barcode_file(cls, barcode_file: BarcodeFile) -> Self:
        
        return cls(
            barcode_file.header.issuer_identification_number,
            barcode_file.header.aamva_version_number,
            barcode_file.header.jurisdiction_version_number)

    @classmethod
    def from_barcode_str(cls, _str: str) -> Self:
        return cls.from_barcode_file(BarcodeFile.from_str(_str))
