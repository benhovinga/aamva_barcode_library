from dataclasses import dataclass
from enum import Flag, auto

class CardType(Flag):
    ID = auto()
    DL = auto()
    BOTH = ID | DL
    
    @staticmethod
    def card_names():
        return {
            CardType.ID: "Identification Card",
            CardType.DL: "Driver License Card"
        }


@dataclass
class CardProfile:
    card_type: CardType
    