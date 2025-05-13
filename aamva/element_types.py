from datetime import datetime, date


def parse_boolean_element(value: str) -> bool:
    """Parses a boolean element. Element value is either "1" (True) or the element is not set (False)."""
    if int(value) == 1:
        return True
    raise ValueError("Boolean element must have a value of 1 or is not set.")


def parse_compliance_type_element(value: str) -> str:
    """Parses the DHS compliance type code."""
    match value.upper():
        case "F":
            return "compliant"
        case "N":
            return "non-compliant"
    raise ValueError(f"Invalid compliance type given: {value}")


def parse_date_element(value: str) -> date:
    """Parses a date string. Dates can be in "YYYYMMDD" format or "MMDDYYYY" format."""
    if len(value) != 8 or not value.isdigit():
        raise ValueError("Invalid date string format. Must be 8 digits.")

    # If the first 4 digits form a plausible year, assume YYYYMMDD
    if 1900 <= int(value[:4]):
        try:
            return datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            raise ValueError("Invalid date in YYYYMMDD format.")
    else:
        # Otherwise, assume MMDDYYYY
        try:
            return datetime.strptime(value, "%m%d%Y").date()
        except ValueError:
            raise ValueError("Invalid date in MMDDYYYY format.")


def parse_eye_color_element(value: str) -> str:
    """Parses the D20 eye color code."""
    match value.upper():
        case "BLK":
            return "Black or very dark brown"
        case "BLU":
            return "Blue"
        case "BRO" | "BRN":
            return "Brown, including amber"
        case "DIC":
            return "Dichromatic or multicolor, of one or both eyes"
        case "GRY":
            return "Gray"
        case "GRN":
            return "Green"
        case "HAZ":
            return "Hazel, a mixture of colors, most commonly green and brown"
        case "MAR":
            return "Maroon"
        case "PNK":
            return "Pink or albino"
        case "UNK":
            return "Unknown"
    raise ValueError(f"Invalid eye color code: {value}")


def parse_hair_color_element(value: str) -> str:
    """Parses the D20 hair color code."""
    match value.upper():
        case "BAL":
            return "Bald"
        case "BLK":
            return "Black"
        case "BLN":
            return "Blond"
        case "BRO" | "BRN":
            return "Brown"
        case "GRY":
            return "Gray"
        case "RED":
            return "Red/Auburn"
        case "SDY":
            return "Sandy"
        case "WHI":
            return "White"
        case "UNK":
            return "Unknown"
    return value


def parse_race_ethnicity_element(value: str) -> str:
    """Parses the D20 race/ethnicity code."""
    match value.upper():
        case "AI":
            return "Alaskan or American Indian"
        case "AP":
            return "Asian or Pacific Islander"
        case "BK":
            return "Black"
        case "H":
            return "Hispanic Origin"
        case "O":
            return "Non-hispanic"
        case "U":
            return "Unknown"
        case "W":
            return "White"
    raise ValueError(f"Invalid race/ethnicity code: {value}")


def parse_sex_element(value: str, aamva_version: int) -> str:
    """Parses the sex element."""
    match int(value):
        case 1:
            return "male"
        case 2:
            return "female"
        case 9:
            if aamva_version < 9:  # Introduced in version 9
                raise ValueError(
                    f"Sex value \"9\" is not defined in version {aamva_version} of the AAMVA DL/ID spec.")
            return "not specified"
    raise ValueError("Invalid sex value. Must be 1, 2, or 9")


def parse_truncation_element(value: str) -> str:
    """Parses a truncation code."""
    match value.upper():
        case "T":
            return "has been truncated"
        case "N":
            return "has not been truncated"
        case "U":
            return "unknown whether truncated"
    raise ValueError(f"Invalid truncation code: {value}")


def parse_weight_range_element(value: str) -> str:
    """Parses the weight range element."""
    match int(value):
        case 0:
            return "up to 31 kg (up to 70 lbs)"
        case 1:
            return "32 - 45 kg (71 - 100 lbs)"
        case 2:
            return "46 - 59 kg (101 - 130 lbs)"
        case 3:
            return "60 - 70 kg (131 - 160 lbs)"
        case 4:
            return "71 - 86 kg (161 - 190 lbs)"
        case 5:
            return "87 - 100 kg (191 - 220 lbs)"
        case 6:
            return "101 - 113 kg (221 - 250 lbs)"
        case 7:
            return "114 - 127 kg (251 - 280 lbs)"
        case 8:
            return "128 - 145 kg (281 - 320 lbs)"
        case 9:
            return "146+ kg (321+ lbs)"
    raise ValueError("Invalid weight range value. Must be a number between 0 and 9")
