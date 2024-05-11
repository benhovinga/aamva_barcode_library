import pytest

import aamva_barcode_file.subfile_designator as subfile_designator


valid_testdata_ids = ("AAVMA Version 1", "AAMVA Version 10")
valid_testdata = (
    # ((test_string, version, (options, ...)), ...)
    (
        # AAMVA Version 1
        "@\n\x1e\rANSI 6360000102DL00390187ZV02260032",
        1,
        (
            {
                "subfile_type": "DL",
                "offset": 39,
                "length": 187
            },
            {
                "subfile_type": "ZV",
                "offset": 226,
                "length": 32
            }
        )
    ),
    (
        # AAMVA Version 10
        "@\n\x1e\rANSI 636000100102DL00410278ZV03190008",
        10,
        (
            {
                "subfile_type": "DL",
                "offset": 41,
                "length": 278
            },
            {
                "subfile_type": "ZV",
                "offset": 319,
                "length": 8
            }
        )
    )
)


@pytest.mark.parametrize("test_string, version, options", valid_testdata, ids=valid_testdata_ids)
def test_can_parse_subfile_designator(test_string, version, options):
    for i in range(len(options)):
        assert subfile_designator.SubfileDesignator.parse(test_string, version, i) == subfile_designator.SubfileDesignator(**options[i])


def test_can_unparse_subfile_designator():
    assert subfile_designator.SubfileDesignator(
        subfile_type="DL",
        offset=12,
        length=321).unparse() == "DL00120321"


def test_parse_raises_index_error_on_short_designator():
    with pytest.raises(IndexError, match="Subfile designator too short."):
        subfile_designator.SubfileDesignator.parse("@\n\x1e\rANSI 6360000102", 1, 0)


def test_parse_raises_value_error_on_bad_data():
    with pytest.raises(ValueError, match="invalid literal for int"):
        subfile_designator.SubfileDesignator.parse("@\n\x1e\rANSI 6360000102XXXXXXXXXX", 1, 0)
