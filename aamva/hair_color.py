from typing import NamedTuple


class HairColor(NamedTuple):
    code: str
    color: str


HAIR_COLORS = (
    HairColor("BAL", "Bald"),
    HairColor("BLK", "Black"),
    HairColor("BLN", "Blond"),
    HairColor("BRO", "Brown"),
    HairColor("GRY", "Gray"),
    HairColor("RED", "Red/Auburn"),
    HairColor("SDY", "Sandy"),
    HairColor("WHI", "White"),
    HairColor("UNK", "Unknown"))


def parse_hair_color(code: str) -> HairColor:
    code = "BRO" if code == "BRN" else code  # Some cards use BRN for Brown
    try:
        return tuple(filter(lambda x: x.code == code, HAIR_COLORS))[0]
    except IndexError:
        raise ValueError(f"Color code '{code}' not found.")
