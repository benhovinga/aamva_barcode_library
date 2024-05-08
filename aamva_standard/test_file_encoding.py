import pytest
import file_encoding

testdata_ids = ("AAMVA Version 1", "AAMVA Version 10")
testdata = (
    # ((test_string, designators, expects), ...)
    (
        # AAMVA Version 1
        "@\n\x1e\rANSI 6360000102DL00390187ZV02260032DLDAQ0123456789ABC\n" +
        "DAAPUBLIC,JOHN,Q\nDAG123 MAIN STREET\nDAIANYTOWN\nDAJVA\n" +
        "DAK123459999  \nDARDM  \nDAS          \nDAT     \nDAU509\nDAW175\n" +
        "DAYBL \nDAZBR \nDBA20011201\nDBB19761123\nDBCM\nDBD19961201\r" +
        "ZVZVAJURISDICTIONDEFINEDELEMENT\r",
        (
            ("DL", 39, 187),
            ("ZV", 226, 32)
        ),
        {
            "header": {
                "data_element_separator": "\n",
                "record_separator": "\x1e",
                "segment_terminator": "\r",
                "issuer_identification_number": 636000,
                "aamva_version_number": 1,
                "jurisdiction_version_number": 0,
                "number_of_entries": 2
            },
            "subfiles": {
                "DL": {
                    "DAQ": "0123456789ABC",
                    "DAA": "PUBLIC,JOHN,Q",
                    "DAG": "123 MAIN STREET",
                    "DAI": "ANYTOWN",
                    "DAJ": "VA",
                    "DAK": "123459999  ",
                    "DAR": "DM  ",
                    "DAS": "          ",
                    "DAT": "     ",
                    "DAU": "509",
                    "DAW": "175",
                    "DAY": "BL ",
                    "DAZ": "BR ",
                    "DBA": "20011201",
                    "DBB": "19761123",
                    "DBC": "M",
                    "DBD": "19961201"
                },
                "ZV": {
                    "ZVA": "JURISDICTIONDEFINEDELEMENT"
                }
            }
        }
    ),
    (
        # AAMVA Version 10
        "@\n\x1e\rANSI 636000100102DL00410278ZV03190008DLDAQT64235789\n" +
        "DCSSAMPLE\nDDEN\nDACMICHAEL\nDDFN\nDADJOHN\nDDGN\nDCUJR\nDCAD\n" +
        "DCBK\nDCDPH\nDBD06062019\nDBB06061986\nDBA12102024\nDBC1\n" +
        "DAU068 in\nDAYBRO\nDAG2300 WEST BROAD STREET\nDAIRICHMOND\nDAJVA\n" +
        "DAK232690000  \nDCF2424244747474786102204\nDCGUSA\nDCK123456789\n" +
        "DDAF\nDDB06062018\nDDC06062020\nDDD1\rZVZVA01\r",
        (
            ("DL", 41, 278),
            ("ZV", 319, 8)
        ),
        {
            "header": {
                "data_element_separator": "\n",
                "record_separator": "\x1e",
                "segment_terminator": "\r",
                "issuer_identification_number": 636000,
                "aamva_version_number": 10,
                "jurisdiction_version_number": 1,
                "number_of_entries": 2
            },
            "subfiles": {
                "DL": {
                    "DAC": "MICHAEL",
                    "DAD": "JOHN",
                    "DAG": "2300 WEST BROAD STREET",
                    "DAI": "RICHMOND",
                    "DAJ": "VA",
                    "DAK": "232690000  ",
                    "DAQ": "T64235789",
                    "DAU": "068 in",
                    "DAY": "BRO",
                    "DBA": "12102024",
                    "DBB": "06061986",
                    "DBC": "1",
                    "DBD": "06062019",
                    "DCA": "D",
                    "DCB": "K",
                    "DCD": "PH",
                    "DCF": "2424244747474786102204",
                    "DCG": "USA",
                    "DCK": "123456789",
                    "DCS": "SAMPLE",
                    "DCU": "JR",
                    "DDA": "F",
                    "DDB": "06062018",
                    "DDC": "06062020",
                    "DDD": "1",
                    "DDE": "N",
                    "DDF": "N",
                    "DDG": "N"
                },
                "ZV": {
                    "ZVA": "01"
                }
            }
        }
    )
)


@pytest.mark.parametrize(
    "version, expects",
    ((1, 19), (2, 21)),
    ids=("AAMVA Version 1", "AAMVA Version 2+"))
def test_header_length_lambda_function(version, expects):
    assert file_encoding.header_length(version) == expects


@pytest.mark.parametrize("test_string, _, expects", testdata, ids=testdata_ids)
def test_can_read_file_header(test_string, _, expects):
    assert file_encoding.parse_file_header(test_string) == expects["header"]


def test_read_file_header_raises_file_type_missing():
    with pytest.raises(ValueError, match="file type missing"):
        file_encoding.parse_file_header("@\n\x1e\rLLLL 999999100201")


@pytest.mark.parametrize(
    "test_string, designators, expects", testdata, ids=testdata_ids)
def test_can_read_subfile_designator(test_string, designators, expects):
    for index, designator in enumerate(designators):
        assert file_encoding.parse_subfile_designator(
            test_string,
            expects["header"]["aamva_version_number"],
            index) == designator


@pytest.mark.parametrize(
    "test_string, designators, expects", testdata, ids=testdata_ids)
def test_can_read_subfile(test_string, designators, expects):
    assert file_encoding.parse_subfile(
        test_string,
        expects["header"]["data_element_separator"],
        expects["header"]["segment_terminator"],
        *designators[0]) == expects["subfiles"]["DL"]
    assert file_encoding.parse_subfile(
        test_string,
        expects["header"]["data_element_separator"],
        expects["header"]["segment_terminator"],
        *designators[1]) == expects["subfiles"]["ZV"]


@pytest.mark.parametrize(
    "test_string, designators, expects", testdata, ids=testdata_ids)
def test_read_subfile_raises_missing_subfile_type(
        test_string, designators, expects):
    with pytest.raises(ValueError, match="missing subfile type"):
        file_encoding.parse_subfile(
            test_string,
            expects["header"]["data_element_separator"],
            expects["header"]["segment_terminator"],
            designators[0][0], designators[0][1] - 1, designators[0][2])


@pytest.mark.parametrize(
    "test_string, designators, expects", testdata, ids=testdata_ids)
def test_read_subfile_raises_missing_segment_terminator(
        test_string, designators, expects):
    with pytest.raises(ValueError, match="missing segment terminator"):
        file_encoding.parse_subfile(
            test_string,
            expects["header"]["data_element_separator"],
            expects["header"]["segment_terminator"],
            designators[0][0], designators[0][1], designators[0][2] - 1)


@pytest.mark.parametrize("test_string, _, expects", testdata, ids=testdata_ids)
def test_can_read_file(test_string, _, expects):
    assert file_encoding.parse_file(test_string) == expects


def test_read_file_raises_number_of_entries_cannot_be_less_than_1():
    with pytest.raises(
            ValueError,
            match="number of entries cannot be less than 1"):
        file_encoding.parse_file("@\n\x1e\rANSI 6360000100")
