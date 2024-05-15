from typing import NamedTuple


class IssuingAuthority(NamedTuple):
    issuer_id: int
    jurisdiction: str
    abbr: str
    country: str


ISSUING_AUTHORITIES = (
    # AAMVA DL/ID Card Design Standard IIN List
    # Source: https://www.aamva.org/identity/issuer-identification-numbers-(iin)
    # Last updated: 2023-12-29
    IssuingAuthority(604426, "Prince Edward Island", "PE", "Canada"),
    IssuingAuthority(604427, "American Samoa", "AS", "USA"),
    IssuingAuthority(604428, "Quebec", "QC", "Canada"),
    IssuingAuthority(604429, "Yukon", "YT", "Canada"),
    IssuingAuthority(604430, "Norther Marianna Islands", "MP", "USA"),
    IssuingAuthority(604431, "Puerto Rico", "PR", "USA"),
    IssuingAuthority(604432, "Alberta", "AB", "Canada"),
    IssuingAuthority(604433, "Nunavut", "NU", "Canada"),
    IssuingAuthority(604434, "Northwest Territories", "NT", "Canada"),
    IssuingAuthority(636000, "Virginia", "VA", "USA"),
    IssuingAuthority(636001, "New York", "NY", "USA"),
    IssuingAuthority(636002, "Massachusetts", "MA", "USA"),
    IssuingAuthority(636003, "Maryland", "MD", "USA"),
    IssuingAuthority(636004, "North Carolina", "NC", "USA"),
    IssuingAuthority(636005, "South Carolina", "SC", "USA"),
    IssuingAuthority(636006, "Connecticut", "CT", "USA"),
    IssuingAuthority(636007, "Louisiana", "LA", "USA"),
    IssuingAuthority(636008, "Montana", "MT", "USA"),
    IssuingAuthority(636009, "New Mexico", "NM", "USA"),
    IssuingAuthority(636010, "Florida", "FL", "USA"),
    IssuingAuthority(636011, "Delaware", "DE", "USA"),
    IssuingAuthority(636012, "Ontario", "ON", "Canada"),
    IssuingAuthority(636013, "Nova Scotia", "NS", "Canada"),
    IssuingAuthority(636014, "California", "CA", "USA"),
    IssuingAuthority(636015, "Texas", "TX", "USA"),
    IssuingAuthority(636016, "Newfoundland", "NF", "Canada"),
    IssuingAuthority(636017, "New Brunswick", "NB", "Canada"),
    IssuingAuthority(636018, "Iowa", "IA", "USA"),
    IssuingAuthority(636019, "Guam", "GU", "USA"),
    IssuingAuthority(636020, "Colorado", "GM", "USA"),
    IssuingAuthority(636021, "Arkansas", "AR", "USA"),
    IssuingAuthority(636022, "Kansas", "KS", "USA"),
    IssuingAuthority(636023, "Ohio", "OH", "USA"),
    IssuingAuthority(636024, "Vermont", "VT", "USA"),
    IssuingAuthority(636025, "Pennsylvania", "PA", "USA"),
    IssuingAuthority(636026, "Arizona", "AZ", "USA"),
    IssuingAuthority(636027, "State Dept. (Diplomatic)", None, "USA"),
    IssuingAuthority(636028, "British Columbia", "BC", "Canada"),
    IssuingAuthority(636029, "Oregon", "OR", "USA"),
    IssuingAuthority(636030, "Missouri", "MO", "USA"),
    IssuingAuthority(636031, "Wisconsin", "WI", "USA"),
    IssuingAuthority(636032, "Michigan", "MI", "USA"),
    IssuingAuthority(636033, "Alabama", "AL", "USA"),
    IssuingAuthority(636034, "North Dakota", "ND", "USA"),
    IssuingAuthority(636035, "Illinois", "IL", "USA"),
    IssuingAuthority(636036, "New Jersey", "NJ", "USA"),
    IssuingAuthority(636037, "Indiana", "IN", "USA"),
    IssuingAuthority(636038, "Minnesota", "MN", "USA"),
    IssuingAuthority(636039, "New Hampshire", "NH", "USA"),
    IssuingAuthority(636040, "Utah", "UT", "USA"),
    IssuingAuthority(636041, "Maine", "ME", "USA"),
    IssuingAuthority(636042, "South Dakota", "SD", "USA"),
    IssuingAuthority(636043, "District of Columbia", "DC", "USA"),
    IssuingAuthority(636044, "Saskatchewan", "SK", "Canada"),
    IssuingAuthority(636045, "Washington", "WA", "USA"),
    IssuingAuthority(636046, "Kentucky", "KY", "USA"),
    IssuingAuthority(636047, "Hawaii", "HI", "USA"),
    IssuingAuthority(636048, "Manitoba", "MB", "Canada"),
    IssuingAuthority(636049, "Nevada", "NV", "USA"),
    IssuingAuthority(636050, "Idaho", "ID", "USA"),
    IssuingAuthority(636051, "Mississippi", "MS", "USA"),
    IssuingAuthority(636052, "Rhode Island", "RI", "USA"),
    IssuingAuthority(636053, "Tennessee", "TN", "USA"),
    IssuingAuthority(636054, "Nebraska", "NE", "USA"),
    IssuingAuthority(636055, "Georgia", "GA", "USA"),
    IssuingAuthority(636056, "Coahuila", "CU", "Mexico"),
    IssuingAuthority(636057, "Hidalgo", "HL", "Mexico"),
    IssuingAuthority(636058, "Oklahoma", "OK", "USA"),
    IssuingAuthority(636059, "Alaska", "AK", "USA"),
    IssuingAuthority(636060, "Wyoming", "WY", "USA"),
    IssuingAuthority(636061, "West Virginia", "WV", "USA"),
    IssuingAuthority(636062, "Virgin Islands", "VI", "USA"),
)


def get_authority_by_id(id_number: int) -> IssuingAuthority:
    try: 
        return tuple(filter(lambda i: i.issuer_id == id_number, ISSUING_AUTHORITIES))[0]
    except IndexError:
        raise ValueError(f"Issuer ID number '{id_number}' not found in authority list.")
