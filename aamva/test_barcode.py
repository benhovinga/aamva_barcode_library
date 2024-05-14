import pytest

import barcode as barcode

barcode_testdata = (
    # ((version, barcode_string, header, designators, subfiles), ...)
    (
        # AAMVA Version 1
        1,
        "@\n\x1e\rANSI 6360000102DL00390187ZV02260032DLDAQ0123456789ABC\n" +
        "DAAPUBLIC,JOHN,Q\nDAG123 MAIN STREET\nDAIANYTOWN\nDAJVA\n" +
        "DAK123459999  \nDARDM  \nDAS          \nDAT     \nDAU509\nDAW175\n" +
        "DAYBL \nDAZBR \nDBA20011201\nDBB19761123\nDBCM\nDBD19961201\r" +
        "ZVZVAJURISDICTIONDEFINEDELEMENT\r",
        (636000, 1, 2, 0),
        (("DL", 39, 187), ("ZV", 226, 32)),
        ()
    ), (
        # AAMVA Version 10
        10,
        "@\n\x1e\rANSI 636000100102DL00410278ZV03190008DLDAQT64235789\n" +
        "DCSSAMPLE\nDDEN\nDACMICHAEL\nDDFN\nDADJOHN\nDDGN\nDCUJR\nDCAD\n" +
        "DCBK\nDCDPH\nDBD06062019\nDBB06061986\nDBA12102024\nDBC1\n" +
        "DAU068 in\nDAYBRO\nDAG2300 WEST BROAD STREET\nDAIRICHMOND\nDAJVA\n" +
        "DAK232690000  \nDCF2424244747474786102204\nDCGUSA\nDCK123456789\n" +
        "DDAF\nDDB06062018\nDDC06062020\nDDD1\rZVZVA01\r",
        (636000, 10, 2, 1),
        (("DL", 41, 278), ("ZV", 319, 8)),
        ()
    )
)
barcode_testdata_ids = tuple(map(lambda v: f"Version {v[0]}", barcode_testdata))


@pytest.fixture
def replace_char_at_index():
    def _replace_char_at_index(self, index):
        self = list(self)
        self[index] = "#"
        return "".join(self)
    return _replace_char_at_index


class TestTrimBeforeFunction:
    def test_should_successfully_trim_everything_before_the_search_character(self):
        assert barcode.trim_before("@", "Before@After") == "@After"
        
    def test_should_work_even_if_not_required(self):
        assert barcode.trim_before("@", "@After") == "@After"
        
    def test_should_not_raise_value_error_when_search_char_not_in_string(self):
        assert barcode.trim_before("@", "It's not here!") == "It's not here!"


class TestHeaderLengthFunction:
    @pytest.mark.parametrize("aamva_version, header_length", ((1, 19), (10, 21)), ids=(1, 10))
    def test_should_return_correct_header_length_for_aamva_version(
        self, aamva_version, header_length):
        assert barcode.header_length(aamva_version) == header_length

    @pytest.mark.parametrize("aamva_version", (-1, 0, 100))
    def test_should_raise_value_error_when_aamva_version_out_of_range(self, aamva_version):
        with pytest.raises(ValueError, match="out of range"):
            barcode.header_length(aamva_version)


class TestParseFileHeaderFunction:
    raises_testdata = tuple(map(lambda x: (x[0], x[1]), barcode_testdata))
    header_testdata = tuple(map(lambda x: (x[1], x[2]), barcode_testdata))
    
    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_header_is_too_short(self, _, barcode_string):
        with pytest.raises(ValueError, match="too short"):
            barcode.parse_file_header(barcode_string[:17])

    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_compliance_indicator_is_invalid(self, _, barcode_string, replace_char_at_index):
        with pytest.raises(ValueError, match="COMPLIANCE_INDICATOR"):
            barcode.parse_file_header(replace_char_at_index(barcode_string, 0))

    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_data_element_separator_is_invalid(self, _, barcode_string, replace_char_at_index):
        with pytest.raises(ValueError, match="DATA_ELEMENT_SEPARATOR"):
            barcode.parse_file_header(replace_char_at_index(barcode_string, 1))

    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_record_separator_is_invalid(self, _, barcode_string, replace_char_at_index):
        with pytest.raises(ValueError, match="RECORD_SEPARATOR"):
            barcode.parse_file_header(replace_char_at_index(barcode_string, 2))

    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_segment_terminator_is_invalid(self, _, barcode_string, replace_char_at_index):
        with pytest.raises(ValueError, match="SEGMENT_TERMINATOR"):
            barcode.parse_file_header(replace_char_at_index(barcode_string, 3))

    @pytest.mark.parametrize("_, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_file_type_is_invalid(self, _, barcode_string, replace_char_at_index):
        with pytest.raises(ValueError, match="FILE_TYPE"):
            barcode.parse_file_header(replace_char_at_index(barcode_string, 4))

    @pytest.mark.parametrize("version, barcode_string", raises_testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_header_is_too_short_for_version(self, version, barcode_string):
        length = barcode.header_length(version)
        with pytest.raises(ValueError, match="too short"):
            barcode.parse_file_header(barcode_string[:length - 1])

    @pytest.mark.parametrize("barcode_string, header", header_testdata, ids=barcode_testdata_ids)
    def test_should_successfully_return_file_header_tuple(self, barcode_string, header):
        assert barcode.parse_file_header(barcode_string) == barcode.FileHeader(*header)
        assert barcode.parse_file_header(barcode_string) == header


class TestParseSubfileDesignatorFunction:
    testdata = tuple(map(lambda x: (x[0], x[1], x[3]), barcode_testdata))
    
    @pytest.mark.parametrize("version, barcode_string, _", testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_designator_too_short(self, version, barcode_string, _):
        length = 28 if version < 2 else 30
        with pytest.raises(ValueError, match="too short"):
            barcode.parse_subfile_designator(barcode_string[:length], version, 0)
    
    @pytest.mark.parametrize("index", (0, 1), ids=("Subfile Designator 0", "Subfile Designator 1"))
    @pytest.mark.parametrize("version, barcode_string, designators", testdata, ids=barcode_testdata_ids)
    def test_should_successfully_return_subfile_designator_tuple(self, version, barcode_string, designators, index):
        assert barcode.parse_subfile_designator(barcode_string, version, index) == designators[index]
        assert barcode.parse_subfile_designator(barcode_string, version, index) == barcode.SubfileDesignator(*designators[index])


class TestParseSubfileFunction:
    testdata = tuple(map(lambda x: (x[1], x[3]), barcode_testdata))
    
    @pytest.mark.parametrize("index", (0, 1), ids=("Subfile 0", "Subfile 1"))
    @pytest.mark.parametrize("barcode_string, designators", testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_subfile_too_short(self, index, barcode_string, designators):
        with pytest.raises(ValueError, match="too short"):
            length = designators[index][1] + designators[index][2] - 1
            barcode.parse_subfile(barcode_string[:length], designators[index])

    @pytest.mark.parametrize("index", (0, 1), ids=("Subfile 0", "Subfile 1"))
    @pytest.mark.parametrize("barcode_string, designators", testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_missing_subfile_type(self, index, barcode_string, designators, replace_char_at_index):
        with pytest.raises(ValueError, match="missing subfile type"):
            barcode_string = replace_char_at_index(barcode_string, designators[index][1])
            barcode.parse_subfile(barcode_string, designators[index])

    @pytest.mark.parametrize("index", (0, 1), ids=("Subfile 0", "Subfile 1"))
    @pytest.mark.parametrize("barcode_string, designators", testdata, ids=barcode_testdata_ids)
    def test_should_raise_value_error_when_missing_segment_terminator(self, index, barcode_string, designators, replace_char_at_index):
        with pytest.raises(ValueError, match="missing segment terminator"):
            subfile_end = designators[index][1] + designators[index][2] - 1
            barcode_string = replace_char_at_index(barcode_string, subfile_end)
            barcode.parse_subfile(barcode_string, designators[index])

