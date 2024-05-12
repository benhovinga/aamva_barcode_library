import pytest

import aamva.card as card


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
