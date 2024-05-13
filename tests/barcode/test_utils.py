import pytest

import aamva.barcode.utils as utils


def test_can_trim_before():
    assert utils.trim_before("@", "@After") == "@After"
    assert utils.trim_before("@", "Before@After") == "@After"
