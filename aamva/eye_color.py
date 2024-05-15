from typing import NamedTuple


class EyeColor(NamedTuple):
    code: str
    color: str
    description: str


EYE_COLORS = (
    EyeColor("BLK", "Black", "Black or very dark brown"),
    EyeColor("BLU", "Blue", "Blue"),
    EyeColor("BRO", "Brown", "Brown, including amber"),
    EyeColor("DIC", "Dichromatic", "Dichromatic or multicolor, of one or both eyes"),
    EyeColor("GRY", "Gray", "Gray"),
    EyeColor("GRN", "Green", "Green"),
    EyeColor("HAZ", "Hazel", "Hazel, a mixture of colors, most commonly green and brown"),
    EyeColor("MAR", "Maroon", "Maroon"),
    EyeColor("PNK", "Pink", "Pink or albino"),
    EyeColor("UNK", "Unknown", "Unknown"))


def parse_eye_color(code: str) -> EyeColor:
    code = "BRO" if code == "BRN" else code  # Some cards use BRN for Brown
    try:
        return tuple(filter(lambda x: x.code == code, EYE_COLORS))[0]
    except IndexError:
        raise ValueError(f"Color code '{code}' not found.")
