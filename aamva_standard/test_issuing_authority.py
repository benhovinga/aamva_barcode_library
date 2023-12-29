import pytest
import issuing_authority


@pytest.fixture
def authority_list():
    return (
        issuing_authority.IssuingAuthority(100001, "Test Jurisdiction 1", "T1", "Canada"),
        issuing_authority.IssuingAuthority(100002, "Test Jurisdiction 2", "T2", "USA")
    )


@pytest.fixture
def fake_authority_list(authority_list):
    saved_list = issuing_authority.ISSUING_AUTHORITIES
    issuing_authority.ISSUING_AUTHORITIES = authority_list
    yield None
    issuing_authority.ISSUING_AUTHORITIES = saved_list


def test_can_get_authority_by_id(fake_authority_list, authority_list):
    assert issuing_authority.get_authority_by_id(100001) == authority_list[0]
    assert issuing_authority.get_authority_by_id(100002) == authority_list[1]
    with pytest.raises(KeyError, match="not found"):
        issuing_authority.get_authority_by_id(1)
