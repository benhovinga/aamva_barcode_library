import pytest
import datetime

from aamva.card.date import Date


testdata_ids = ("Canada's date format", "Mexico's date format", "USA's date format")
testdata = (
    # ((unparsed, country, parsed), ...)
    ("20240512", "Canada", (2024, 5, 12)),
    ("20240512", "Mexico", (2024, 5, 12)),
    ("05122024", "USA", (2024, 5, 12)))


@pytest.mark.parametrize("unparsed, country, parsed", testdata, ids=testdata_ids)
def test_can_parse_country_date(unparsed, country, parsed):
    assert Date.parse_country_date(unparsed, country) == datetime.date(*parsed)


@pytest.mark.parametrize("unparsed, country, parsed", testdata, ids=testdata_ids)
def test_can_unparse_country_date(unparsed, country, parsed):
    assert Date(*parsed).unparse_country_date(country) == unparsed


@pytest.mark.parametrize("unparsed, country, parsed", testdata, ids=testdata_ids)
def test_can_unparse_country_datetime(unparsed, country, parsed):
    assert Date.unparse_country_date(datetime.date(*parsed), country) == unparsed
