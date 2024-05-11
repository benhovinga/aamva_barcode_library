import pytest

import aamva_barcode_file.subfile as subfile


testdata_ids = ("1 element", "multi element", "multi element with empty")
testdata = (
    # ((test_string, designator, expects), ...)
    (
        "DLAAA123\r",
        ("DL", 0, 9),
        ("DL", {"AAA":"123"})
    ),
    (
        "DLAAA123\nBBBsomething here\r",
        ("DL", 0, 27),
        ("DL", {"AAA":"123", "BBB":"something here"})
    ),
    (
        "DLAAA123\nBBBsomething here\n\r",
        ("DL", 0, 28),
        ("DL", {"AAA":"123", "BBB":"something here"})
    ),
)


@pytest.mark.parametrize("test_string, designator, expects", testdata, ids=testdata_ids)
def test_can_parse_subfile(test_string, designator, expects):
    assert subfile.Subfile.parse(test_string, subfile.SubfileDesignator(*designator)) == subfile.Subfile(*expects)


def test_parse_raises_value_error_on_missing_subfile_type():
    with pytest.raises(ValueError, match="Subfile is missing subfile type."):
        subfile.Subfile.parse("DDAAA123\r", subfile.SubfileDesignator("DL", 0, 9))


def test_parse_raises_value_error_on_missing_segment_terminator():
    with pytest.raises(ValueError, match="Subfile is missing segment terminator."):
        subfile.Subfile.parse("DLAAA123", subfile.SubfileDesignator("DL", 0, 8))
