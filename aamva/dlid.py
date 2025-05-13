from datetime import date
from typing import NamedTuple

from .barcode import Subfile
from .element_types import parse_boolean_element, parse_compliance_type_element, parse_date_element, parse_eye_color_element, parse_hair_color_element, parse_race_ethnicity_element, parse_sex_element, parse_truncation_element, parse_weight_range_element


class Property(NamedTuple):
    name: str
    value: str | int | date | bool


class DLIDDecoder:
    def __init__(self, aamva_version: int):
        if aamva_version < 1 or aamva_version > 10:
            raise ValueError("AAMVA version must be number 1-10.")
        self.aamva_version = aamva_version

    def decode_single_element(self, id: str, value: str) -> Property:
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
                    return ("eye_color", parse_eye_color_element(value))
                return ("physical_description_eye_color", parse_eye_color_element(value))

            case "DAZ":  # Version 1+
                return ("hair_color", parse_hair_color_element(value))

            case "DBA":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_license_expiration_date", parse_date_element(value))
                return ("document_expiration_date", parse_date_element(value))

            case "DBB":  # Version 1+
                return ("date_of_birth", parse_date_element(value))

            case "DBC":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_sex", parse_sex_element(value, self.aamva_version))
                return ("physical_description_sex", parse_sex_element(value, self.aamva_version))

            case "DBD":  # Version 1+
                if self.aamva_version == 1:
                    return ("driver_license_or_id_document_issue_date", parse_date_element(value))
                return ("document_issue_date", parse_date_element(value))

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
                    return ("physical_description_weight_range", parse_weight_range_element(value))

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
                    return ("race_ethnicity", parse_race_ethnicity_element(value))

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
                    return ("compliance_type", parse_compliance_type_element(value))

            case "DDB":  # Version 4+
                if self.aamva_version >= 4:
                    return ("card_revision_date", parse_date_element(value))

            case "DDC":  # Version 4+
                if self.aamva_version >= 4:
                    return ("hazmat_endorsement_expiration_date", parse_date_element(value))

            case "DDD":  # Version 4+
                if self.aamva_version >= 4:
                    return ("limited_duration_document_indicator", parse_boolean_element(value))

            case "DDE":  # Version 4+
                if self.aamva_version >= 4:
                    return ("family_name_truncation", parse_truncation_element(value))

            case "DDF":  # Version 4+
                if self.aamva_version >= 4:
                    return ("first_name_truncation", parse_truncation_element(value))

            case "DDG":  # Version 4+
                if self.aamva_version >= 4:
                    return ("middle_name_truncation", parse_truncation_element(value))

            case "DDH":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_18_until", parse_date_element(value))

            case "DDI":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_19_until", parse_date_element(value))

            case "DDJ":  # Version 5+
                if self.aamva_version >= 5:
                    return ("under_21_until", parse_date_element(value))

            case "DDK":  # Version 6+
                if self.aamva_version >= 6:
                    return ("organ_donor_indicator", parse_boolean_element(value))

            case "DDL":  # Version 7+
                if self.aamva_version >= 7:
                    return ("veteran_indicator", parse_boolean_element(value))

            case "PAA":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_classification_code", value)

            case "PAB":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_expiration_date", value)

            case "PAC":  # Version 1
                if self.aamva_version == 1:
                    return ("permit_identifier", value)

            case "PAD":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_issue_date", value)

            case "PAE":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_restriction_code", value)

            case "PAF":  # Version 1
                if self.aamva_version == 1:
                    return ("driver_permit_endorsement_code", value)

        raise ValueError(f"Element ID \"{id}\" is not defined in version {self.aamva_version} of the AAMVA DL/ID spec.")

    # TODO: Is not rubust yet
    def decode_subfile(self, subfile: Subfile) -> dict:
        if subfile["subfile_type"] not in ("DL", "ID"):
            raise ValueError("Unsupported subfile type")

        profile = {}
        for key, value in subfile["elements"].items():
            prop = self.decode_single_element(key, value)
            profile[prop[0]] = prop[1]

        return profile
