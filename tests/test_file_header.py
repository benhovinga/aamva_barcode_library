import pytest

import aamva_barcode_file.file_header as file_header
import aamva_barcode_file.errors as errors


header_length_testdata_ids = ("AAMVA Version 1", "AAMVA Version 10")
header_length_testdata = (
    # ((aamva_version, expects), ...)
    (1, 19),
    (10, 21)
)


@pytest.mark.parametrize("aamva_version, expects", header_length_testdata, ids=header_length_testdata_ids)
def test_header_length_static_method(aamva_version, expects):
    assert file_header.FileHeader.header_length(aamva_version) == expects


valid_testdata_ids = ("AAVMA Version 1", "AAMVA Version 10")
valid_testdata = (
    # ((test_string, options), ...)
    (
        # AAMVA Version 1
        "@\n\x1e\rANSI 6360000102",
        {
            "issuer_id": 636000,
            "aamva_version": 1,
            "number_of_entries": 2
        }
    ),
    (
        # AAMVA Version 10
        "@\n\x1e\rANSI 636000100102",
        {
            "issuer_id": 636000,
            "aamva_version": 10,
            "number_of_entries": 2,
            "jurisdiction_version": 1
        }
    )
)


@pytest.mark.parametrize("test_string, options", valid_testdata, ids=valid_testdata_ids)
def test_can_parse_file_header(test_string, options):
    assert file_header.FileHeader.parse(test_string) == file_header.FileHeader(**options)


@pytest.mark.parametrize("test_string, options", valid_testdata, ids=valid_testdata_ids)
def test_can_unparse_file_header(test_string, options):
    assert file_header.FileHeader(**options).unparse() == test_string


length_testdata_ids = (
    "Test MIN_LENGTH",
    "Test AAMVA Version 1",
    "Test AAMVA Version 10"
)
length_testdata = (
    "@\n\x1e\rANSI 6360000",
    "@\n\x1e\rANSI 636000010",
    "@\n\x1e\rANSI 63600010010"
)


@pytest.mark.parametrize("test_string", length_testdata, ids=length_testdata_ids)
def test_parse_raises_index_error_on_short_header(test_string):
    with pytest.raises(IndexError, match="Header length is too short."):
        file_header.FileHeader.parse(test_string)


def test_parse_raises_invalid_header_error_on_compliance_indicator():
    with pytest.raises(errors.InvalidHeaderError, match="COMPLIANCE_INDICATOR"):
        file_header.FileHeader.parse("#\n\x1e\rANSI 636000100102")


def test_parse_raises_invalid_header_error_on_data_element_separator():
    with pytest.raises(errors.InvalidHeaderError, match="DATA_ELEMENT_SEPARATOR"):
        file_header.FileHeader.parse("@#\x1e\rANSI 636000100102")


def test_parse_raises_invalid_header_error_on_record_separator():
    with pytest.raises(errors.InvalidHeaderError, match="RECORD_SEPARATOR"):
        file_header.FileHeader.parse("@\n#\rANSI 636000100102")


def test_parse_raises_invalid_header_error_on_segment_terminator():
    with pytest.raises(errors.InvalidHeaderError, match="SEGMENT_TERMINATOR"):
        file_header.FileHeader.parse("@\n\x1e#ANSI 636000100102")


def test_parse_raises_invalid_header_error_on_file_type():
    with pytest.raises(errors.InvalidHeaderError, match="FILE_TYPE"):
        file_header.FileHeader.parse("@\n\x1e\r#####636000100102")

