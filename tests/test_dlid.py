import pytest
import datetime

import aamva.dlid as dlid

parametrize_aamva_version = pytest.mark.parametrize(
    argnames="aamva_version",
    argvalues=range(1, 11),
    ids=(f"aamva_version={i}" for i in range(1, 11)))


class TestDLIDDecoderClass:
    @parametrize_aamva_version
    def test_can_initialize_decoder_class(self, aamva_version):
        decoder = dlid.DLIDDecoder(aamva_version)
        assert decoder is not None
        assert isinstance(decoder, dlid.DLIDDecoder)
        assert decoder.aamva_version == aamva_version

    @pytest.mark.parametrize("aamva_version", (0, 11))
    def test_should_raise_value_error_when_given_invalid_version(self, aamva_version):
        with pytest.raises(ValueError, match="version must be number 1-10"):
            dlid.DLIDDecoder(aamva_version)


@parametrize_aamva_version
class TestParseBooleanElementMethod:
    def test_should_return_true(self, aamva_version):
        assert dlid.DLIDDecoder(aamva_version).parse_boolean_element("1") == True

    def test_should_raise_value_error_when_given_anything_else(self, aamva_version):
        with pytest.raises(ValueError, match="must have a value of 1 or is not set"):
            dlid.DLIDDecoder(aamva_version).parse_boolean_element("0")


@parametrize_aamva_version
class TestParseComplianceTypeElementMethod:
    @pytest.mark.parametrize("value, expects", (("F", "compliant"), ("N", "non-compliant")))
    def test_should_return_correct_type(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_compliance_type_element(value) == expects

    def test_should_raise_value_error_when_given_anything_else(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid compliance type given"):
            dlid.DLIDDecoder(aamva_version).parse_compliance_type_element("R")


@parametrize_aamva_version
class TestParseDateElementMethod:
    @pytest.mark.parametrize("value, expects", (
        ("20241231", datetime.date(2024, 12, 31)),
        ("12312024", datetime.date(2024, 12, 31))), ids=("YYYYMMDD", "MMDDYYYY"))
    def test_should_return_correct_date_object(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_date_element(value) == expects

    @pytest.mark.parametrize("value, error_msg", (
        ("13322024", "Invalid date in MMDDYYYY format"),
        ("19322024", "Invalid date in YYYYMMDD format"),
        ("1234567", "Invalid date string format"),
        ("abcdefgh", "Invalid date string format")), ids=("MMDDYYYY", "YYYYMMDD", "short", "alpha"))
    def test_should_raise_value_error_when_given_bad_date_format(self, aamva_version, value, error_msg):
        with pytest.raises(ValueError, match=error_msg):
            dlid.DLIDDecoder(aamva_version).parse_date_element(value)


@parametrize_aamva_version
class TestParseEyeColorElementMethod:
    @pytest.mark.parametrize("value, expects", (
        ("BLK", "Black or very dark brown"),
        ("BLU", "Blue"),
        ("BRO", "Brown, including amber"),
        ("BRN", "Brown, including amber"),
        ("DIC", "Dichromatic or multicolor, of one or both eyes"),
        ("GRY", "Gray"),
        ("GRN", "Green"),
        ("HAZ", "Hazel, a mixture of colors, most commonly green and brown"),
        ("MAR", "Maroon"),
        ("PNK", "Pink or albino"),
        ("UNK", "Unknown")))
    def test_should_return_correct_eye_color(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_eye_color_element(value) == expects

    def test_should_raise_value_error_when_given_bad_code(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid eye color code"):
            dlid.DLIDDecoder(aamva_version).parse_eye_color_element("RGB")


@parametrize_aamva_version
class TestParseHairColorElementMethod:
    @pytest.mark.parametrize("value, expects", (
        ("BAL", "Bald"),
        ("BLK", "Black"),
        ("BLN", "Blond"),
        ("BRO", "Brown"),
        ("BRN", "Brown"),
        ("GRY", "Gray"),
        ("RED", "Red/Auburn"),
        ("SDY", "Sandy"),
        ("WHI", "White"),
        ("UNK", "Unknown")))
    def test_should_return_correct_hair_color(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_hair_color_element(value) == expects

    def test_should_return_unmodified_value_if_not_in_list(self, aamva_version):
        assert dlid.DLIDDecoder(aamva_version).parse_hair_color_element("Blond") == "Blond"


@parametrize_aamva_version
class TestParseRaceEthnicityElementMethod:
    @pytest.mark.parametrize("value, expects", (
        ("AI", "Alaskan or American Indian"),
        ("AP", "Asian or Pacific Islander"),
        ("BK", "Black"),
        ("H", "Hispanic Origin"),
        ("O", "Non-hispanic"),
        ("U", "Unknown"),
        ("W", "White")))
    def test_should_return_correct_race_ethnicity(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_race_ethnicity_element(value) == expects

    def test_should_raise_value_error_when_given_bad_code(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid race/ethnicity code"):
            dlid.DLIDDecoder(aamva_version).parse_race_ethnicity_element("PL")


@parametrize_aamva_version
class TestParseSexElementMethod:
    @pytest.mark.parametrize("value, expects", ((1, "male"), (2, "female"), (9, "not specified")))
    def test_should_return_correct_sex(self, aamva_version, value, expects):
        if value == 9 and aamva_version < 9:
            pytest.skip("unsupported version")
        assert dlid.DLIDDecoder(aamva_version).parse_sex_element(value) == expects

    def test_should_raise_value_error_when_version_does_not_support_not_specified(self, aamva_version):
        if aamva_version >= 9:
            pytest.skip("supported version")
        with pytest.raises(ValueError, match="is not defined in version"):
            dlid.DLIDDecoder(aamva_version).parse_sex_element(9)

    def test_should_raise_value_error_when_given_invalid_value(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid sex value"):
            dlid.DLIDDecoder(aamva_version).parse_sex_element(3)


@parametrize_aamva_version
class TestParseTruncationElementMethod:
    @pytest.mark.parametrize("value, expects", (("T", "has been truncated"), ("N", "has not been truncated"), ("U", "unknown whether truncated")))
    def test_should_return_correct_truncation(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_truncation_element(value) == expects

    def test_should_raise_value_error_when_given_invalid_value(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid truncation code"):
            dlid.DLIDDecoder(aamva_version).parse_truncation_element("A")


@parametrize_aamva_version
class TestParseWeightRangeElementMethod:
    @pytest.mark.parametrize("value, expects", (
        ("0", "up to 31 kg (up to 70 lbs)"),
        ("1", "32 - 45 kg (71 - 100 lbs)"),
        ("2", "46 - 59 kg (101 - 130 lbs)"),
        ("3", "60 - 70 kg (131 - 160 lbs)"),
        ("4", "71 - 86 kg (161 - 190 lbs)"),
        ("5", "87 - 100 kg (191 - 220 lbs)"),
        ("6", "101 - 113 kg (221 - 250 lbs)"),
        ("7", "114 - 127 kg (251 - 280 lbs)"),
        ("8", "128 - 145 kg (281 - 320 lbs)"),
        ("9", "146+ kg (321+ lbs)")
    ))
    def test_should_return_correct_weight_range(self, aamva_version, value, expects):
        assert dlid.DLIDDecoder(aamva_version).parse_weight_range_element(value) == expects

    def test_should_raise_value_error_when_given_invalid_value(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid weight range value"):
            dlid.DLIDDecoder(aamva_version).parse_weight_range_element("10")


property_test_matrix = (
    # (id, (*versions,), type, property_name)
    ("DAA", (1,), "string", "driver_license_name"),
    ("DAB", (1,), "string", "driver_last_name"),
    ("DAC", (1,), "string", "driver_first_name"),
    ("DAC", (4, 5, 6, 7, 8, 9, 10), "string", "customer_first_name"),
    ("DAD", (1,), "string", "driver_middle_name_or_initial"),
    ("DAD", (4, 5, 6, 7, 8, 9, 10), "string", "customer_middle_names"),
    ("DAE", (1,), "string", "driver_name_suffix"),
    ("DAF", (1,), "string", "driver_name_prefix"),
    ("DAG", (1,), "string", "driver_mailing_street_address_1"),
    ("DAG", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "address_street_1"),
    ("DAH", (1,), "string", "driver_mailing_street_address_2"),
    ("DAH", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "address_street_2"),
    ("DAI", (1,), "string", "driver_mailing_city"),
    ("DAI", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "address_city"),
    ("DAJ", (1,), "string", "driver_mailing_jurisdiction_code"),
    ("DAJ", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "address_jurisdiction_code"),
    ("DAK", (1,), "string", "driver_mailing_postal_code"),
    ("DAK", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "address_postal_code"),
    ("DAL", (1,), "string", "driver_residence_street_address_1"),
    ("DAM", (1,), "string", "driver_residence_street_address_2"),
    ("DAN", (1,), "string", "driver_residence_city"),
    ("DAO", (1,), "string", "driver_residence_jurisdiction_code"),
    ("DAP", (1,), "string", "driver_residence_postal_code"),
    ("DAQ", (1,), "string", "driver_license_id_number"),
    ("DAQ", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "customer_id_number"),
    ("DAR", (1,), "string", "driver_license_classification_code"),
    ("DAS", (1,), "string", "driver_license_restriction_code"),
    ("DAT", (1,), "string", "driver_license_endorsements_code"),
    ("DAU", (1,), "number", "height_ft_in"),
    ("DAU", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "physical_description_height"),
    ("DAV", (1,), "number", "height_cm"),
    ("DAW", (1,), "number", "weight_lbs"),
    ("DAW", (4, 5, 6, 7, 8, 9, 10), "number", "weight_pounds"),
    ("DAX", (1,), "number", "weight_kg"),
    ("DAX", (4, 5, 6, 7, 8, 9, 10), "number", "weight_kilograms"),
    ("DAY", (1,), "eye_color", "eye_color"),
    ("DAY", (2, 3, 4, 5, 6, 7, 8, 9, 10), "eye_color", "physical_description_eye_color"),
    ("DAZ", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), "hair_color", "hair_color"),
    ("DBA", (1,), "date", "driver_license_expiration_date"),
    ("DBA", (2, 3, 4, 5, 6, 7, 8, 9, 10), "date", "document_expiration_date"),
    ("DBB", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), "date", "date_of_birth"),
    ("DBC", (1,), "sex", "driver_sex"),
    ("DBC", (2, 3, 4, 5, 6, 7, 8, 9, 10), "sex", "physical_description_sex"),
    ("DBD", (1,), "date", "driver_license_or_id_document_issue_date"),
    ("DBD", (2, 3, 4, 5, 6, 7, 8, 9, 10), "date", "document_issue_date"),
    ("DBE", (1,), "string", "issue_timestamp"),
    ("DBF", (1,), "string", "number_of_duplicates"),
    ("DBG", (1,), "string", "medical_indicator_codes"),
    ("DBG", (3, 4, 5, 6, 7, 8, 9, 10), "string", "alias_aka_given_name"),
    ("DBH", (1,), "string", "organ_donor"),
    ("DBI", (1,), "string", "non_resident_indicator"),
    ("DBJ", (1,), "string", "unique_customer_identifier"),
    ("DBK", (1,), "string", "social_security_number"),
    ("DBL", (1,), "string", "driver_aka_date_of_birth"),
    ("DBM", (1,), "string", "driver_aka_social_security_number"),
    ("DBN", (1,), "string", "driver_aka_name"),
    ("DBN", (2,), "string", "alias_aka_name"),
    ("DBN", (3, 4, 5, 6, 7, 8, 9, 10), "string", "alias_aka_family_name"),
    ("DBO", (1,), "string", "driver_aka_last_name"),
    ("DBP", (1,), "string", "driver_aka_first_name"),
    ("DBQ", (1,), "string", "driver_aka_middle_name"),
    ("DBR", (1,), "string", "driver_aka_suffix"),
    ("DBS", (1,), "string", "driver_aka_prefix"),
    ("DBS", (3, 4, 5, 6, 7, 8, 9, 10), "string", "alias_aka_suffix_name"),
    ("DCA", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_vehicle_class"),
    ("DCB", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_restriction_codes"),
    ("DCD", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_endorsement_codes"),
    ("DCE", (2, 3, 4, 5, 6, 7, 8, 9, 10), "weight_range", "physical_description_weight_range"),
    ("DCF", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "document_discriminator"),
    ("DCG", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "country_identification"),
    ("DCH", (2, 3), "string", "federal_commercial_vehicle_codes"),
    ("DCI", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "place_of_birth"),
    ("DCJ", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "audit_information"),
    ("DCK", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "inventory_control_number"),
    ("DCL", (2, 3, 4, 5, 6, 7, 8, 9, 10), "race", "race_ethnicity"),
    ("DCM", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "standard_vehicle_classification"),
    ("DCN", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "standard_endorsement_code"),
    ("DCO", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "standard_restriction_code"),
    ("DCP", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_vehicle_classification_description"),
    ("DCQ", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_endorsement_code_description"),
    ("DCR", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "jurisdiction_specific_restriction_code_description"),
    ("DCS", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "customer_family_name"),
    ("DCT", (2, 3), "string", "customer_given_names"),
    ("DCU", (2, 3, 4, 5, 6, 7, 8, 9, 10), "string", "name_suffix"),
    ("DDA", (4, 5, 6, 7, 8, 9, 10), "compliance_type", "compliance_type"),
    ("DDB", (4, 5, 6, 7, 8, 9, 10), "date", "card_revision_date"),
    ("DDC", (4, 5, 6, 7, 8, 9, 10), "date", "hazmat_endorsement_expiration_date"),
    ("DDD", (4, 5, 6, 7, 8, 9, 10), "boolean", "limited_duration_document_indicator"),
    ("DDE", (4, 5, 6, 7, 8, 9, 10), "truncation", "family_name_truncation"),
    ("DDF", (4, 5, 6, 7, 8, 9, 10), "truncation", "first_name_truncation"),
    ("DDG", (4, 5, 6, 7, 8, 9, 10), "truncation", "middle_name_truncation"),
    ("DDH", (5, 6, 7, 8, 9, 10), "date", "under_18_until"),
    ("DDI", (5, 6, 7, 8, 9, 10), "date", "under_19_until"),
    ("DDJ", (5, 6, 7, 8, 9, 10), "date", "under_21_until"),
    ("DDK", (6, 7, 8, 9, 10), "boolean", "organ_donor_indicator"),
    ("DDL", (7, 8, 9, 10), "boolean", "veteran_indicator"),
    ("PAA", (1,), "string", "driver_permit_classification_code"),
    ("PAB", (1,), "string", "driver_permit_expiration_date"),
    ("PAC", (1,), "string", "permit_identifier"),
    ("PAD", (1,), "string", "driver_permit_issue_date"),
    ("PAE", (1,), "string", "driver_permit_restriction_code"),
    ("PAF", (1,), "string", "driver_permit_endorsement_code"),
)


class TestDecodeSingleElementMethod:
    @parametrize_aamva_version
    @pytest.mark.parametrize(
        argnames="id, versions, test_type, property_name",
        argvalues=property_test_matrix,
        ids=(f"id={i[0]}-property_name={i[3]}" for i in property_test_matrix))
    def test_should_return_a_valid_property_tuple(self, aamva_version, id, versions, test_type, property_name):
        if aamva_version not in versions:
            pytest.skip("unsupported version")
        match test_type:
            case "string":
                value = "A simple string"
                expects = "A simple string"
            case "number":
                value = "12345"
                expects = 12345
            case "eye_color":
                value = "BLU"
                expects = "Blue"
            case "hair_color":
                value = "BLK"
                expects = "Black"
            case "date":
                value = "20241225"
                expects = datetime.date(2024, 12, 25)
            case "sex":
                value = "1"
                expects = "male"
            case "weight_range":
                value = "1"
                expects = "32 - 45 kg (71 - 100 lbs)"
            case "race":
                value = "W"
                expects = "White"
            case "compliance_type":
                value = "F"
                expects = "compliant"
            case "boolean":
                value = "1"
                expects = True
            case "truncation":
                value = "T"
                expects = "has been truncated"
            case _:
                raise ValueError(f"unknown test type: {test_type}")
        assert dlid.DLIDDecoder(aamva_version).decode_single_element(
            id, value) == dlid.Property(property_name, expects)

    def test_should_raise_value_error_when_given_invalid_id(self):
        with pytest.raises(ValueError, match="not defined in version"):
            dlid.DLIDDecoder(1).decode_single_element("NNN", "")


# TODO: Create tests for each version
class TestDecodeSubfileMethod:
    def test_should_return_a_profile_dict(self):
        assert dlid.DLIDDecoder(10).decode_subfile({
            "subfile_type": "DL",
            "elements": {
                "DAC": "John",
                "DAD": "Middle",
                "DCS": "Smith"
            }
        })  # TODO: Evaluate this against something

    def test_should_raise_value_error_when_given_wrong_subfile_type(self):
        with pytest.raises(ValueError, match="Unsupported subfile type"):
            dlid.DLIDDecoder(10).decode_subfile({
                "subfile_type": "AA",
                "elements": {"AAA": "BAD VALUE"}
            })
