import pytest

import aamva.race_ethnicity as race_ethnicity

race_ehtnicity_testdata = (
    # ((test, expects), ...)
    ("AI", ("AI", "Alaskan or American Indian")),
    ("AP", ("AP", "Asian or Pacific Islander")),
    ("BK", ("BK", "Black")),
    ("H", ("H", "Hispanic Origin")),
    ("O", ("O", "Non-hispanic")),
    ("U", ("U", "Unknown")),
    ("W", ("W", "White")))


class TestParseRaceEthnicityFunction:
    @pytest.mark.parametrize("test, expects", race_ehtnicity_testdata, ids=tuple(map(lambda x: x[0], race_ehtnicity_testdata)))
    def test_should_successfully_return_race_ethnicity_tuple(self, test, expects):
        assert race_ethnicity.parse_race_ethnicity(test) == expects
        assert type(race_ethnicity.parse_race_ethnicity(test)) == race_ethnicity.RaceEthnicity

    def test_should_raise_value_error_when_code_not_found(self):
        with pytest.raises(ValueError, match='not found'):
            race_ethnicity.parse_race_ethnicity("AAA")
