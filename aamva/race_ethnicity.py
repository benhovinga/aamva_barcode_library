from typing import NamedTuple


class RaceEthnicity(NamedTuple):
    code: str
    description: str


RACE_ETHNICITIES = (
    RaceEthnicity("AI", "Alaskan or American Indian"),
    RaceEthnicity("AP", "Asian or Pacific Islander"),
    RaceEthnicity("BK", "Black"),
    RaceEthnicity("H", "Hispanic Origin"),
    RaceEthnicity("O", "Non-hispanic"),
    RaceEthnicity("U", "Unknown"),
    RaceEthnicity("W", "White"))


def parse_race_ethnicity(code: str) -> RaceEthnicity:
    try:
        return tuple(filter(lambda x: x.code == code, RACE_ETHNICITIES))[0]
    except IndexError:
        raise ValueError(f"Race/Ethnicity code '{code}' not found.")
