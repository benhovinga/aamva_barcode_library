from enum import Enum
from typing import Self


class Card(Enum):
    DRIVER_LICENSE = "DL"
    IDENTIFICATION_CARD = "ID"
    BOTH = DRIVER_LICENSE, IDENTIFICATION_CARD


class Sex(Enum):
    MALE = 1
    FEMALE = 2
    NOT_SPECIFIED = 9


class EyeColor(Enum):
    BLACK = "BLK"
    BLUE = "BLU"
    BROWN = "BRO"
    DICHROMATIC = "DIC"
    GRAY = "GRY"
    GREEN = "GRN"
    HAZEL = "HAZ"
    MAROON = "MAR"
    PINK = "PNK"
    UNKNOWN = "UNK"


class HairColor(Enum):
    BALD = "bald"
    BLACK = "black"
    BLOND = "blond"
    BROWN = "brown"
    GRAY = "gray"
    RED_AUBURN = "red/auburn"
    SANDY = "sandy"
    WHITE = "white"
    UNKNOWN = "unknown"


class HairColorD20(Enum):
    BALD = "BAL"
    BLACK = "BLK"
    BLOND = "BLN"
    BROWN = "BRO"
    GRAY = "GRY"
    RED_AUBURN = "RED"
    SANDY = "SDY"
    WHITE = "WHI"
    UNKNOWN = "UNK"


class NameTruncation(Enum):
    TRUNCATED = "T"
    NOT_TRUNCATED = "N"
    UNKNOWN = "U"


class WeightRange(Enum):
    GROUP_0 = "up to 31 kg (up to 70 lbs)"
    GROUP_1 = "32 - 45 kg (71 - 100 lbs)"
    GROUP_2 = "46 - 59 kg (101 - 130 lbs)"
    GROUP_3 = "60 - 70 kg (131 - 160 lbs)"
    GROUP_4 = "71 - 86 kg (161 - 190 lbs)"
    GROUP_5 = "87 - 100 kg (191 - 220 lbs)"
    GROUP_6 = "101 - 113 kg (221 - 250 lbs)"
    GROUP_7 = "114 - 127 kg (251 - 280 lbs)"
    GROUP_8 = "128 - 145 kg (281 - 320 lbs)"
    GROUP_9 = "146+ kg (321+ lbs)"
    
    def to_int(self) -> int:
        return tuple(self.__class__).index(self)
    
    @classmethod
    def from_int(cls, _int: int) -> Self:
        return tuple(cls)[_int]


class RaceEthnicity(Enum):
    AI = "Alaskan or American Indian"
    AP = "Asian or Pacific Islander"
    BK = "Black"
    H = "Hispanic Origin"
    O = "Non-hispanic"
    U = "Unknown"
    W = "White"
    

class ComplianceType(Enum):
    COMPLIANT = "F"
    NON_COMPLIANT = "N"

    def is_compliant(self):
        return True if self == ComplianceType.COMPLIANT else False
