import pytest

import aamva.barcode_file as barcode_file

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
        barcode_file.BarcodeFile(
            header=barcode_file.FileHeader(
                issuer_id=636000,
                aamva_version=1,
                jurisdiction_version=0,
                number_of_entries=2
            ),
            subfiles=(
                barcode_file.Subfile(
                    "DL",
                    {
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
                    }
                ),
                barcode_file.Subfile(
                    "ZV",
                    {
                        "ZVA": "JURISDICTIONDEFINEDELEMENT"
                    }
                )
            )
        )
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
        barcode_file.BarcodeFile(
            header=barcode_file.FileHeader(
                issuer_id=636000,
                aamva_version=10,
                jurisdiction_version=1,
                number_of_entries=2
            ),
            subfiles=(
                barcode_file.Subfile(
                    "DL",
                    {
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
                    }
                ),
                barcode_file.Subfile(
                    "ZV",
                    {
                        "ZVA": "01"
                    }
                )
            )
        )
    )
)


@pytest.mark.parametrize("test_string, _, expects", testdata, ids=testdata_ids)
def test_can_parse_barcode_file(test_string, _, expects):
    assert barcode_file.BarcodeFile.parse(test_string) == expects


def test_parse_raises_value_error_number_of_entries_cannot_be_less_than_1():
    with pytest.raises(
            ValueError,
            match="number of entries cannot be less than 1"):
        barcode_file.BarcodeFile.parse("@\n\x1e\rANSI 6360000100")
