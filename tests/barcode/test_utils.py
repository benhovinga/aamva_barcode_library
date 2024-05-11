import pytest

import aamva.barcode_file.utils as utils


def test_can_trim_before():
    assert utils.trim_before("@", "@After") == "@After"
    assert utils.trim_before("@", "Before@After") == "@After"
    
    
def test_trim_before_raises_typeerror():
    with pytest.raises(TypeError):
        utils.trim_before("@@", "Before@After")


def test_trim_before_raises_valueerror():
    with pytest.raises(ValueError):
        utils.trim_before("@", "Before-After")
