from dataclasses import dataclass, field
import datetime

from old_stuff.Enums import Card, Sex, EyeColor, HairColor, HairColorD20, NameTruncation, WeightRange, RaceEthnicity, ComplianceType


@dataclass(frozen=True)
class ElementField:
    code: str
    name: str
    length: int
    card: Card = field(default=Card.BOTH)
    mandatory: bool = field(default=True)
    fixed: bool = field(default=True)


@dataclass(frozen=True)
class StringField(ElementField):
    fixed: bool = field(default=False)
    
    @staticmethod
    def decode(_str: str) -> str:
        return str(_str)
    
    def encode(self, _str: str) -> str:
        if len(_str) > self.length: _str = _str[:self.length]
        return _str.ljust(self.length) if self.fixed else _str


@dataclass(frozen=True)
class IntField(ElementField):
    @staticmethod
    def decode(_str: str) -> int:
        return int(_str)
    
    def encode(self, _int: int) -> str:
        return str(_int).rjust(self.length, "0")


@dataclass(frozen=True)
class BoolField(ElementField):
    length: int = field(default=1)
    @staticmethod
    def decode(_str: str) -> bool:
        return bool(int(_str))
    
    def encode(self, _bool: bool) -> str:
        return str(int(_bool))


@dataclass(frozen=True)
class DateField(ElementField):
    length: int = field(default=8)

    @staticmethod
    def decoded(_str: str, is_usa: bool = False) -> datetime.date:
        if is_usa:
            return datetime.date(int(_str[0:2]), int(_str[2:4]), int(_str[4:8]))
        return datetime.date(int(_str[0:4]), int(_str[4:6]), int(_str[6:8]))
    
    def encoded(self, _date: datetime.date, is_usa: bool = False) -> str:
        return _date.strftime("%m%d%Y") if is_usa else _date.strftime("%Y%m%d")


@dataclass(frozen=True)
class SexField(ElementField):
    length: int = field(default=1)

    @staticmethod
    def decode(_str: str) -> Sex:
        return Sex(int(_str))
    
    def encode(self, sex: Sex) -> str:
        return str(sex.value)


@dataclass(frozen=True)
class EyeColorField(ElementField):
    length: int = field(default=3)
    
    @staticmethod
    def decode(_str: str) -> EyeColor:
        return EyeColor(_str)
    
    def encode(self, eye_color: EyeColor) -> str:
        return str(eye_color.value)


@dataclass(frozen=True)
class HeightField(ElementField):
    length: int = field(default=6)
    
    @staticmethod
    def decode(_str: str) -> tuple[int,str]:
        return int(_str[:3]), _str[3:].strip()
    
    def encode(self, _tuple: tuple[int,str]) -> str:
        return str(_tuple[0]).rjust(3,"0") + _tuple[1].rjust(3).lower()


@dataclass(frozen=True)
class NameTruncationField(ElementField):
    length: int = field(default=1)
    
    @staticmethod
    def decode(_str: str) -> NameTruncation:
        return NameTruncation(_str.upper())
    
    def encode(self, truncation: NameTruncation) -> str:
        return truncation.value


@dataclass(frozen=True)
class HairColorField(ElementField):
    length: int = field(default=12)
    fixed: int = field(default=False)
    
    @staticmethod
    def decode(_str: str) -> HairColor | HairColorD20:
        return HairColor(_str.lower()) if len(_str) > 3 else HairColorD20(_str.upper())
    
    def encode(self, hair_color: HairColor | HairColorD20) -> str:
        return str(hair_color.value)


@dataclass(frozen=True)
class WeightRangeField(ElementField):
    length: int = field(default=1)
    
    @staticmethod
    def decode(_str: str) -> WeightRange:
        return WeightRange.from_int(int(_str))
    
    def encode(self, weight_range: WeightRange) -> str:
        return str(weight_range.to_int())


@dataclass(frozen=True)
class RaceEthnicityField(ElementField):
    length: int = field(default=3)
    fixed: bool = field(default=False)
    
    @staticmethod
    def decode(_str: str) -> RaceEthnicity:
        return RaceEthnicity[_str]
    
    def encode(self, race_ethnicity: RaceEthnicity) -> str:
        return str(race_ethnicity.name)


@dataclass(frozen=True)
class ComplianceTypeField(ElementField):
    length: int = field(default=1)
    
    @staticmethod
    def decode(_str: str) -> ComplianceType:
        return ComplianceType(_str.upper())
    
    def encode(self, compliance_type: ComplianceType) -> str:
        return str(compliance_type.value)


MANDATORY_FIELDS = (
    StringField("DCA", "jurisdiction_specific_vehicle_class", 6, Card.DRIVER_LICENSE),
    StringField("DCB", "jurisdiction_specific_restriction_codes", 12, Card.DRIVER_LICENSE),
    StringField("DCD", "jurisdiction_specific_endorsement_codes", 5, Card.DRIVER_LICENSE),
    DateField("DBA", "document_expiration_date"),
    StringField("DCS", "customer_family_name", 40),
    StringField("DAC", "customer_first_name", 40),
    StringField("DAD", "customer_middle_name", 40),
    DateField("DBD", "document_issue_date"),
    DateField("DBB", "date_of_birth"),
    SexField("DBC", "physical_description_sex"),
    EyeColorField("DAY", "physical_description_eye_color"),
    HeightField("DAU", "physical_description_height"),
    StringField("DAG", "address_street_1", 35),
    StringField("DAI", "address_city", 20, True, True, ["DL", "ID"]),
    StringField("DAJ", "address_jurisdiction_code", 2, fixed=True),
    StringField("DAK", "address_postal_code", 11, fixed=True),
    StringField("DAQ", "customer_id_number", 25),
    StringField("DCF", "document_discriminator", 25),
    StringField("DCG", "country_identification", 3, fixed=True),
    NameTruncationField("DDE", "family_name_truncation"),
    NameTruncationField("DDF", "first_name_truncation"),
    NameTruncationField("DDG", "middle_name_truncation"),)

_opt = {"mandatory": False}
OPTIONAL_FIELDS = (
    StringField("DAH", "address_street_2", 35, **_opt),
    HairColorField("DAZ", "hair_color", **_opt),
    StringField("DCI", "place_of_birth", 33, **_opt),
    StringField("DCJ", "audit_information", 25, **_opt),
    StringField("DCK", "inventory_control_number", 25, **_opt),
    StringField("DBN", "alias_aka_family_name", 10, **_opt),
    StringField("DBG", "alias_aka_given_name", 15, **_opt),
    StringField("DBS", "alias_aka_suffix_name", 5, **_opt),
    StringField("DCU", "name_suffix", 5, **_opt),
    WeightRangeField("DCE", "physical_description_weight_range", **_opt),
    RaceEthnicityField("DCL", "race_ethnicity", **_opt),
    StringField("DCM", "standard_vehicle_classification", 4, Card.DRIVER_LICENSE, fixed=True, **_opt),   # TODO: Implement Standard
    StringField("DCN", "standard_endorsement_code", 5, Card.DRIVER_LICENSE, fixed=True, **_opt),    # TODO: Implement Standard
    StringField("DCO", "standard_restriction_code", 5, Card.DRIVER_LICENSE, fixed=True, **_opt),    # TODO: Implement Standard
    StringField("DCP", "jurisdiction_specific_vehicle_classification_description", 50, Card.DRIVER_LICENSE, **_opt),
    StringField("DCQ", "jurisdiction_specific_vehicle_endorsement_code_description", 50, Card.DRIVER_LICENSE, **_opt),
    StringField("DCR", "jurisdiction_specific_vehicle_restriction_code_description", 50, Card.DRIVER_LICENSE, **_opt),
    ComplianceTypeField("DDA", "compliance_type", **_opt),
    DateField("DDB", "card_revision_date", **_opt),
    DateField("DDC", "hazmat_endorsement_expiration_date", card=Card.DRIVER_LICENSE, **_opt),
    BoolField("DDD", "limited_duration_document_indicator", **_opt),
    IntField("DAW", "weight_pounds", 3, **_opt),
    IntField("DAX", "weight_kilograms", 3, **_opt),
    DateField("DDH", "under_18_until", **_opt),
    DateField("DDI", "under_19_until", **_opt),
    DateField("DDJ", "under_21_until", **_opt),
    BoolField("DDK", "organ_donor", **_opt),
    BoolField("DDL", "veteran_indicator", **_opt),)

FIELDS = MANDATORY_FIELDS + OPTIONAL_FIELDS
