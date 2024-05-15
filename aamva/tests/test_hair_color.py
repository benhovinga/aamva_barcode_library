import pytest

import aamva.hair_color as hair_color

hair_color_testdata = (
    # ((test, expects), ...)
    ("BAL", ("BAL", "Bald")),
    ("BLK", ("BLK", "Black")),
    ("BLN", ("BLN", "Blond")),
    ("BRO", ("BRO", "Brown")),
    ("BRN", ("BRO", "Brown")),
    ("GRY", ("GRY", "Gray")),
    ("RED", ("RED", "Red/Auburn")),
    ("SDY", ("SDY", "Sandy")),
    ("WHI", ("WHI", "White")),
    ("UNK", ("UNK", "Unknown")))


class TestParseHairColorFunction:
    @pytest.mark.parametrize("test, expects", hair_color_testdata, ids=tuple(map(lambda x: x[0], hair_color_testdata)))
    def test_should_successfully_return_hair_color_tuple(self, test, expects):
        assert hair_color.parse_hair_color(test) == expects
        assert type(hair_color.parse_hair_color(test)) == hair_color.HairColor

    def test_should_raise_value_error_when_code_not_found(self):
        with pytest.raises(ValueError, match='not found'):
            hair_color.parse_hair_color("AAA")
