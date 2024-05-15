import pytest

import aamva.issuing_authority as issuing_authority


issuing_authority_testdata = (
    (100001, "Test Jurisdiction 1", "T1", "Canada"),
    (100002, "Test Jurisdiction 2", "T2", "USA"))


@pytest.fixture
def fake_authority_list():
    saved_authorities = issuing_authority.ISSUING_AUTHORITIES
    replacement_authorities = tuple(map(lambda x: issuing_authority.IssuingAuthority(*x), issuing_authority_testdata))
    issuing_authority.ISSUING_AUTHORITIES = replacement_authorities
    yield None
    issuing_authority.ISSUING_AUTHORITIES = saved_authorities


@pytest.mark.parametrize("issuer_id, jurisdiction, abbr, country", issuing_authority_testdata)
def test_can_get_authority_by_id(fake_authority_list, issuer_id, jurisdiction, abbr, country):
    assert issuing_authority.get_authority_by_id(issuer_id) == (issuer_id, jurisdiction, abbr, country)


def test_should_raise_value_error_when_id_not_found():
    with pytest.raises(ValueError, match="not found"):
        issuing_authority.get_authority_by_id(1)
