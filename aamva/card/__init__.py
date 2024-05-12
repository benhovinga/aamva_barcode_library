from dataclasses import dataclass
from enum import Flag, auto

class CardType(Flag):
    ID = auto()
    DL = auto()
    BOTH = ID | DL
    
    @property
    def description(self):
        if self is CardType.ID:
            return "Identification Card"
        elif self is CardType.DL:
            return "Driver License Card"
        return None


@dataclass
class CardProfile:
    card_type: CardType
    