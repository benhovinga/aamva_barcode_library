from datetime import datetime, date
from typing import Tuple

PropertyName = str
PropertyValue = str | int | date | bool


class Decoder:
    def __init__(self, aamva_version: int):
        self.aamva_version = aamva_version
        self.validation_errors = []

    def parse_boolean_element(self, value: str) -> bool:
        """Parses a boolean element. Element value is either "1" (True) or the element is not set (False)."""
        if int(value) == 1:
            return True
        raise ValueError("Boolean element must have a value of 1 or is not set.")

    def parse_compliance_type_element(self, value: str) -> str:
        """Parses the DHS compliance type code."""
        match value.upper():
            case "F":
                return "compliant"
            case "N":
                return "non-compliant"
        raise ValueError(f"Invalid compliance type given: {value}")

    def parse_date_element(self, value: str) -> date:
        """Parses a date string. Dates can be in YYYYMMDD or MMDDYYYY format."""
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

    def parse_eye_color_element(self, value: str) -> str:
        """Parses the D20 eye color code."""
        match value.upper():
            case "BLK":
                return "Black or very dark brown"
            case "BLU":
                return "Blue"
            case "BRO" | "BRN":
                return "Brown, including amber"
            case "DIC":
                return "Dichromatic", "Dichromatic or multicolor, of one or both eyes"
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

    def parse_hair_color_element(self, value: str) -> str:
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
                return "Uknown"
        return value

    def parse_race_ethnicity_element(self, value: str) -> str:
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

    def parse_sex_element(self, value: str) -> str:
        """Parses the sex element."""
        match int(value):
            case 1:
                return "male"
            case 2:
                return "female"
            case 9:
                return "not specified"
        raise ValueError("Invalid sex value. Must be 1, 2, or 9")

    def parse_truncation_element(self, value: str) -> str:
        """Parses a truncation code."""
        match value.upper():
            case "T":
                return "has been truncated"
            case "N":
                return "has not been truncated"
            case "U":
                return "unknown whether truncated"
        raise ValueError(f"Invalid truncation code: {value}")

    def parse_weight_range_element(self, value: str) -> str:
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

    def decode_single_element(self, id: str, value: str) -> Tuple[PropertyName, PropertyValue]:
        value = value.strip()
        match id.upper():
            case "DAA":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_license_name", value)

            case "DAB":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_last_name", value)

            case "DAC":  # Version 1 or 4+
                if self.aamva_version == 1:
                    return ("driver_first_name", value)
                elif self.aamva_version >= 4:
                    return ("customer_first_name", value)

            case "DAD":  # Version 1 or 4+
                if self.aamva_version == 1:
                    return ("driver_middle_name_or_initial", value)
                elif self.aamva_version >= 4:
                    return ("customer_middle_names", value)

            case "DAE":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_name_suffix", value)

            case "DAF":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_name_prefix", value)

            case "DAG":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_mailing_street_address_1", value)
                return ("address_street_1", value)

            case "DAH":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_mailing_street_address_2", value)
                return ("address_street_2", value)

            case "DAI":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_mailing_city", value)
                return ("address_city", value)

            case "DAJ":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_mailing_jurisdiction_code", value)
                return ("address_jurisdiction_code", value)

            case "DAK":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_mailing_postal_code", value)
                return ("address_postal_code", value)

            case "DAL":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_residence_street_address_1", value)

            case "DAM":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_residence_street_address_2", value)

            case "DAN":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_residence_city", value)

            case "DAO":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_residence_jurisdiction_code", value)

            case "DAP":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_residence_postal_code", value)

            case "DAQ":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_license_id_number", value)
                return ("customer_id_number", value)

            case "DAR":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_license_classification_code", value)

            case "DAS":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_license_restriction_code", value)

            case "DAT":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_license_endorsements_code", value)

            case "DAU":  # Version 1+
                if self.aamva_version == 1:
                    return ("height_ft_in", int(value))
                return ("physical_description_height", value)

            case "DAV":  # Version 1
                if self.aamva_version == 1:
                    return ("height_cm", int(value))

            case "DAW":  # Version 1 or 4+
                if self.aamva_version == 1:
                    return ("weight_lbs", int(value))
                elif self.aamva_version >= 4:
                    return ("weight_pounds", int(value))

            case "DAX":  # Version 1 or 4+
                if self.aamva_version == 1:
                    return ("weight_kg", int(value))
                elif self.aamva_version >= 4:
                    return ("weight_kilograms", int(value))

            case "DAY":  # Version 1+
                if self.aamva_version == 1:
                    return ("eye_color", self.parse_eye_color_element(value))
                return ("physical_description_eye_color", self.parse_eye_color_element(value))

            case "DAZ":  # Version 1+
                return ("hair_color", self.parse_hair_color_element(value))

            case "DBA":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_license_expiration_date", self.parse_date_element(value))
                return ("document_expiration_date", self.parse_date_element(value))

            case "DBB":  # Version 1+
                return ("date_of_birth", self.parse_date_element(value))

            case "DBC":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_sex", self.parse_sex_element(value))
                return ("physical_description_sex", self.parse_sex_element(value))

            case "DBD":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_license_or_id_document_issue_date", self.parse_date_element(value))
                return ("document_issue_date", self.parse_date_element(value))

            case "DBE":  # Version 1
                if self.aamva_version == 1:
                    return ("issue_timestamp", value)

            case "DBF":  # Version 1
                if self.aamva_version == 1:
                    return ("number_of_duplicates", value)

            case "DBG":  # Version 1 or 3+
                if self.aamva_version == 1:
                    return ("medical_indicator_codes", value)
                elif self.aamva_version >= 3:
                    return ("alias_aka_given_name", value)

            case "DBH":  # Version 1
                if self.aamva_version == 1:
                    return ("organ_donor", value)

            case "DBI":  # Version 1
                if self.aamva_version == 1:
                    return ("non_resident_indicator", value)

            case "DBJ":  # Version 1
                if self.aamva_version == 1:
                    return ("unique_customer_identifier", value)

            case "DBK":  # Version 1
                if self.aamva_version == 1:
                    return ("social_security_number", value)

            case "DBL":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_date_of_birth", value)

            case "DBM":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_social_security_number", value)

            case "DBN":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_aka_name", value)
                elif self.aamva_version == 2:
                    return ("alias_aka_name", value)
                return ("alias_aka_family_name", value)

            case "DBO":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_last_name", value)

            case "DBP":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_first_name", value)

            case "DBQ":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_middle_name", value)

            case "DBR":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_aka_suffix", value)

            case "DBS":  # Version 1 or 3+
                if self.aamva_version == 1:
                    return ("driver_aka_prefix", value)
                elif self.aamva_version >= 3:
                    return ("alias_aka_suffix_name", value)

            case "DCA":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_vehicle_class", value)

            case "DCB":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_restriction_codes", value)

            case "DCD":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_endorsement_codes", value)

            case "DCE":  # Version 2+
                if self.aamva_version >= 2:
                    return ("physical_description_weight_range", self.parse_weight_range_element(value))

            case "DCF":  # Version 2+
                if self.aamva_version >= 2:
                    return ("document_discriminator", value)

            case "DCG":  # Version 2+
                if self.aamva_version >= 2:
                    return ("country_identification", value)

            case "DCH":  # Version 2 or 3
                if self.aamva_version == 2 or self.aamva_version == 3:
                    return ("federal_commercial_vehicle_codes", value)

            case "DCI":  # Version 2+
                if self.aamva_version >= 2:
                    return ("place_of_birth", value)

            case "DCJ":  # Version 2+
                if self.aamva_version >= 2:
                    return ("audit_information", value)

            case "DCK":  # Version 2+
                if self.aamva_version >= 2:
                    return ("inventory_control_number", value)

            case "DCL":  # Version 2+
                if self.aamva_version >= 2:
                    return ("race_ethnicity", self.parse_race_ethnicity_element(value))

            case "DCM":  # Version 2+
                if self.aamva_version >= 2:
                    return ("standard_vehicle_classification", value)

            case "DCN":  # Version 2+
                if self.aamva_version >= 2:
                    return ("standard_endorsement_code", value)

            case "DCO":  # Version 2+
                if self.aamva_version >= 2:
                    return ("standard_restriction_code", value)

            case "DCP":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_vehicle_classification_description", value)

            case "DCQ":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_endorsement_code_description", value)

            case "DCR":  # Version 2+
                if self.aamva_version >= 2:
                    return ("jurisdiction_specific_restriction_code_description", value)

            case "DCS":  # Version 2+
                if self.aamva_version >= 2:
                    return ("customer_family_name", value)

            case "DCT":  # Version 2 or 3
                if self.aamva_version == 2 or self.aamva_version == 3:
                    return ("customer_given_names", value)

            case "DCU":  # Version 2+
                if self.aamva_version >= 2:
                    return ("name_suffix", value)

            case "DDA":  # Version 4+
                if self.aamva_version >= 4:
                    return ("compliance_type", self.parse_compliance_type_element(value))

            case "DDB":  # Version 4+
                if self.aamva_version >= 4:
                    return ("card_revision_date", self.parse_date_element(value))

            case "DDC":  # Version 4+
                if self.aamva_version >= 4:
                    return ("hazmat_endorsement_expiration_date", self.parse_date_element(value))

            case "DDD":  # Version 4+
                if self.aamva_version >= 4:
                    return ("limited_duration_document_indicator", self.parse_boolean_element(value))

            case "DDE":  # Version 4+
                if self.aamva_version >= 4:
                    return ("family_name_truncation", self.parse_truncation_element(value))

            case "DDF":  # Version 4+
                if self.aamva_version >= 4:
                    return ("first_name_truncation", self.parse_truncation_element(value))

            case "DDG":  # Version 4+
                if self.aamva_version >= 4:
                    return ("middle_name_truncation", self.parse_truncation_element(value))

            case "DDH":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_18_until", self.parse_date_element(value))

            case "DDH":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_19_until", self.parse_date_element(value))

            case "DDH":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_21_until", self.parse_date_element(value))

            case "DDK":  # Version 6+
                if self.aamva_version >= 6:
                    return ("organ_donor_indicator", self.parse_boolean_element(value))

            case "DDL":  # Version 7+
                if self.aamva_version >= 7:
                    return ("veteran_indicator", self.parse_boolean_element(value))

            case "PAA":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_classification_code")

            case "PAB":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_expiration_date")

            case "PAC":  # Version 1
                if self.aamva_version == 1:
                    return ("permit_identifier")

            case "PAD":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_issue_date")

            case "PAE":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_restriciton_code")

            case "PAF":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_endorsement_code")

        raise ValueError(f"Element ID \"{id}\" is not defined in version {self.aamva_version} of the AAMVA DL/ID spec.")
