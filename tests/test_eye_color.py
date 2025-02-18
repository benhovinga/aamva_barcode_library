import pytest

import aamva.eye_color as eye_color

eye_color_testdata = (
    # ((test, expects), ...)
    ("BLK", ("BLK", "Black", "Black or very dark brown")),
    ("BLU", ("BLU", "Blue", "Blue")),
    ("BRO", ("BRO", "Brown", "Brown, including amber")),
    ("BRN", ("BRO", "Brown", "Brown, including amber")),  # Test conversion to BRO
    ("DIC", ("DIC", "Dichromatic", "Dichromatic or multicolor, of one or both eyes")),
    ("GRY", ("GRY", "Gray", "Gray")),
    ("GRN", ("GRN", "Green", "Green")),
    ("HAZ", ("HAZ", "Hazel", "Hazel, a mixture of colors, most commonly green and brown")),
    ("MAR", ("MAR", "Maroon", "Maroon")),
    ("PNK", ("PNK", "Pink", "Pink or albino")),
    ("UNK", ("UNK", "Unknown", "Unknown")))


class TestParseEyeColorFunction:
    @pytest.mark.parametrize("test, expects", eye_color_testdata, ids=tuple(map(lambda x: x[0], eye_color_testdata)))
    def test_should_successfully_return_eye_color_tuple(self, test, expects):
        assert eye_color.parse_eye_color(test) == expects
        assert type(eye_color.parse_eye_color(test)) == eye_color.EyeColor

    def test_should_raise_value_error_when_code_not_found(self):
        with pytest.raises(ValueError, match='not found'):
            eye_color.parse_eye_color("AAA")
