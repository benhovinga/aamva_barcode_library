from datetime import datetime, date

ISO_FORMAT = "%Y%m%d"
IMPERIAL_FORMAT = "%m%d%Y"


def country_date_format(country: str) -> str:
    country = country.upper()
    match country:
        case "CANADA":
            return ISO_FORMAT
        case "MEXICO":
            return ISO_FORMAT
        case "USA":
            return IMPERIAL_FORMAT
    raise ValueError("Provided country is not supported.")


def parse_date(date_string: str, format: str) -> date:
    try:
        return datetime.strptime(date_string, format).date()
    except:
        raise ValueError("Invalid date format for provided date string.")
