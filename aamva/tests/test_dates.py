import pytest
import datetime

import aamva.dates as dates

country_format_testdata = (
    # ((country, expects), ...)
    ("Canada", "%Y%m%d"),
    ("Mexico", "%Y%m%d"),
    ("USA", "%m%d%Y"))
country_format_testdata_ids = tuple(map(lambda x: x[0], country_format_testdata))


class TestCountryDateFormatFunction:
    def test_should_raise_value_error_when_given_unsupported_country(self):
        with pytest.raises(ValueError, match="not supported"):
            dates.country_date_format("England")

    @pytest.mark.parametrize("country, expects", country_format_testdata, ids=country_format_testdata_ids)
    def test_should_successfully_return_correct_country_format(self, country, expects):
        assert dates.country_date_format(country) == expects


date_testdata = (
    # ((*args, expects), ...)
    (("20240516", "%Y%m%d"), datetime.date(2024, 5, 16)),  # ISO
    (("05162024", "%m%d%Y"), datetime.date(2024, 5, 16)))  # Imperial
date_testdata_ids = ("ISO", "Imperial")


class TestParseDateFunction:
    @pytest.mark.parametrize("args, expects", date_testdata, ids=date_testdata_ids)
    def test_should_successfully_return_date_object(self, args, expects):
        assert dates.parse_date(*args) == expects
    
    def test_should_raise_value_error_when_invalid_date_format(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            dates.parse_date("05162024", "%Y%m%d")
