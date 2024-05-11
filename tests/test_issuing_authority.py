import pytest

import aamva.issuing_authority as issuing_authority


@pytest.fixture
def issuing_authorities_testdata():
    return (
        issuing_authority.IssuingAuthority(
            100001, "Test Jurisdiction 1", "T1", "Canada"),
        issuing_authority.IssuingAuthority(
            100002, "Test Jurisdiction 2", "T2", "USA")
    )


@pytest.fixture
def fake_authority_list(issuing_authorities_testdata):
    saved_authorities = issuing_authority.ISSUING_AUTHORITIES
    issuing_authority.ISSUING_AUTHORITIES = issuing_authorities_testdata
    yield None
    issuing_authority.ISSUING_AUTHORITIES = saved_authorities


def test_get_authority_by_id(
        fake_authority_list, issuing_authorities_testdata):
    assert (issuing_authority.get_authority_by_id(100001) ==
            issuing_authorities_testdata[0])
    assert (issuing_authority.get_authority_by_id(100002) ==
            issuing_authorities_testdata[1])
    with pytest.raises(issuing_authority.IssuingAuthorityNotFound):
        issuing_authority.get_authority_by_id(1)
