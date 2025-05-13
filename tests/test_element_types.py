import pytest
import datetime

import aamva.element_types as element_types


class TestParseBooleanElementFunction:
    def test_should_return_true(self):
        assert element_types.parse_boolean_element("1") == True

    def test_should_raise_value_error_when_given_anything_else(self):
        with pytest.raises(ValueError, match="must have a value of 1 or is not set"):
            element_types.parse_boolean_element("0")


class TestParseComplianceTypeElementFunction:
    @pytest.mark.parametrize("value, expects", (("F", "compliant"), ("N", "non-compliant")))
    def test_should_return_correct_type(self, value, expects):
        assert element_types.parse_compliance_type_element(value) == expects

    def test_should_raise_value_error_when_given_anything_else(self):
        with pytest.raises(ValueError, match="Invalid compliance type given"):
            element_types.parse_compliance_type_element("R")


class TestParseDateElementFunction:
    @pytest.mark.parametrize("value, expects", (
        ("20241231", datetime.date(2024, 12, 31)),
        ("12312024", datetime.date(2024, 12, 31))), ids=("YYYYMMDD", "MMDDYYYY"))
    def test_should_return_correct_date_object(self, value, expects):
        assert element_types.parse_date_element(value) == expects

    @pytest.mark.parametrize("value, error_msg", (
        ("13322024", "Invalid date in MMDDYYYY format"),
        ("19322024", "Invalid date in YYYYMMDD format"),
        ("1234567", "Invalid date string format"),
        ("abcdefgh", "Invalid date string format")), ids=("MMDDYYYY", "YYYYMMDD", "short", "alpha"))
    def test_should_raise_value_error_when_given_bad_date_format(self, value, error_msg):
        with pytest.raises(ValueError, match=error_msg):
            element_types.parse_date_element(value)


class TestParseEyeColorElementFunction:
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
    def test_should_return_correct_eye_color(self, value, expects):
        assert element_types.parse_eye_color_element(value) == expects

    def test_should_raise_value_error_when_given_bad_code(self):
        with pytest.raises(ValueError, match="Invalid eye color code"):
            element_types.parse_eye_color_element("RGB")


class TestParseHairColorElementFunction:
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
    def test_should_return_correct_hair_color(self, value, expects):
        assert element_types.parse_hair_color_element(value) == expects

    def test_should_return_unmodified_value_if_not_in_list(self):
        assert element_types.parse_hair_color_element("Blond") == "Blond"


class TestParseRaceEthnicityElementFunction:
    @pytest.mark.parametrize("value, expects", (
        ("AI", "Alaskan or American Indian"),
        ("AP", "Asian or Pacific Islander"),
        ("BK", "Black"),
        ("H", "Hispanic Origin"),
        ("O", "Non-hispanic"),
        ("U", "Unknown"),
        ("W", "White")))
    def test_should_return_correct_race_ethnicity(self, value, expects):
        assert element_types.parse_race_ethnicity_element(value) == expects

    def test_should_raise_value_error_when_given_bad_code(self):
        with pytest.raises(ValueError, match="Invalid race/ethnicity code"):
            element_types.parse_race_ethnicity_element("PL")


@pytest.mark.parametrize(
    argnames="aamva_version",
    argvalues=range(1, 11),
    ids=(f"aamva_version={i}" for i in range(1, 11)))
class TestParseSexElementFunction:
    @pytest.mark.parametrize("value, expects", ((1, "male"), (2, "female"), (9, "not specified")))
    def test_should_return_correct_sex(self, aamva_version, value, expects):
        if value == 9 and aamva_version < 9:
            pytest.skip("unsupported version")
        assert element_types.parse_sex_element(value, aamva_version) == expects

    def test_should_raise_value_error_when_version_does_not_support_sex_option(self, aamva_version):
        if aamva_version >= 9:
            pytest.skip("supported version")
        with pytest.raises(ValueError, match="is not defined in version"):
            element_types.parse_sex_element(9, aamva_version)

    def test_should_raise_value_error_when_given_invalid_value(self, aamva_version):
        with pytest.raises(ValueError, match="Invalid sex value"):
            element_types.parse_sex_element(3, aamva_version)


class TestParseTruncationElementFunction:
    @pytest.mark.parametrize("value, expects", (("T", "has been truncated"), ("N", "has not been truncated"), ("U", "unknown whether truncated")))
    def test_should_return_correct_truncation(self, value, expects):
        assert element_types.parse_truncation_element(value) == expects

    def test_should_raise_value_error_when_given_invalid_value(self):
        with pytest.raises(ValueError, match="Invalid truncation code"):
            element_types.parse_truncation_element("A")


class TestParseWeightRangeElementFunction:
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
    def test_should_return_correct_weight_range(self, value, expects):
        assert element_types.parse_weight_range_element(value) == expects

    def test_should_raise_value_error_when_given_invalid_value(self):
        with pytest.raises(ValueError, match="Invalid weight range value"):
            element_types.parse_weight_range_element("10")
