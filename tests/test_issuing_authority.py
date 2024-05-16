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


class TestGetAuthorityByIdFunction:
    @pytest.mark.parametrize("issuer_id, jurisdiction, abbr, country", issuing_authority_testdata, ids=(0, 1))
    def test_should_successfully_return_issuing_authority_tuple(self, fake_authority_list, issuer_id, jurisdiction, abbr, country):
        assert issuing_authority.get_authority_by_id(issuer_id) == (issuer_id, jurisdiction, abbr, country)
        assert type(issuing_authority.get_authority_by_id(issuer_id)) == issuing_authority.IssuingAuthority

    def test_should_raise_value_error_when_id_not_found(self):
        with pytest.raises(ValueError, match="not found"):
            issuing_authority.get_authority_by_id(1)
