from datetime import datetime, date

ISO_FORMAT = "%Y%m%d"
IMPERIAL_FORMAT = "%m%d%Y"


def country_date_format(country: str) -> str:
    country = country.upper()
    if country == "CANADA":
        return ISO_FORMAT
    elif country == "MEXICO":
        return ISO_FORMAT
    elif country == "USA":
        return IMPERIAL_FORMAT
    raise ValueError("Provided country is not supported.")


def get_date_format(aamva_version: int, country: str) -> str:
    # AAMVA Version 3 introduced ISO date format option, prior versions only used Imperial format.
    return IMPERIAL_FORMAT if aamva_version < 3 else country_date_format(country)


def parse_date(date_string: str, format: str) -> date:
    try:
        return datetime.strptime(date_string, format).date()
    except ValueError:
        raise ValueError("Invalid date format for provided date string.")
