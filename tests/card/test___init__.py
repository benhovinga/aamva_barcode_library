import pytest

import aamva.card as card

EXAMPLE_DATA = (
    # AAMVA Version 1
    "@\n\x1e\rANSI 6360000102DL00390187ZV02260032DLDAQ0123456789ABC\n" +
    "DAAPUBLIC,JOHN,Q\nDAG123 MAIN STREET\nDAIANYTOWN\nDAJVA\n" +
    "DAK123459999  \nDARDM  \nDAS          \nDAT     \nDAU509\nDAW175\n" +
    "DAYBL \nDAZBR \nDBA20011201\nDBB19761123\nDBCM\nDBD19961201\r" +
    "ZVZVAJURISDICTIONDEFINEDELEMENT\r",
    
    # AAMVA Version 10
    "@\n\x1e\rANSI 636000100102DL00410278ZV03190008DLDAQT64235789\n" +
    "DCSSAMPLE\nDDEN\nDACMICHAEL\nDDFN\nDADJOHN\nDDGN\nDCUJR\nDCAD\n" +
    "DCBK\nDCDPH\nDBD06062019\nDBB06061986\nDBA12102024\nDBC1\n" +
    "DAU068 in\nDAYBRO\nDAG2300 WEST BROAD STREET\nDAIRICHMOND\nDAJVA\n" +
    "DAK232690000  \nDCF2424244747474786102204\nDCGUSA\nDCK123456789\n" +
    "DDAF\nDDB06062018\nDDC06062020\nDDD1\rZVZVA01\r")


def test_card_type_enums():
    assert card.CardType.ID.value == 1
    assert card.CardType.DL.value == 2
    assert card.CardType.BOTH.value == 3
    assert card.CardType.ID in card.CardType.BOTH
    assert card.CardType.DL in card.CardType.BOTH


def test_card_type_descriptions():
    assert card.CardType.ID.description == "Identification Card"
    assert card.CardType.DL.description == "Driver License Card"
    assert card.CardType.BOTH.description == None
