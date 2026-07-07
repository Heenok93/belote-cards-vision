from dataclasses import dataclass
from enum import Enum
from typing import List


# =========================================================
# SUITS
# =========================================================

class Suit(Enum):
    COEUR = "COEUR"
    CARREAU = "CARREAU"
    PIQUE = "PIQUE"
    TREFLE = "TREFLE"


# =========================================================
# CARD VALUES
# =========================================================

class Value(Enum):
    SEPT = "7"
    HUIT = "8"
    NEUF = "9"
    DIX = "10"
    VALET = "VALET"
    DAME = "DAME"
    ROI = "ROI"
    AS = "AS"


# =========================================================
# CARD DATACLASS
# =========================================================

@dataclass(frozen=True)
class Card:
    value: Value
    suit: Suit

    # -----------------------------------------------------
    # STRING REPRESENTATION
    # -----------------------------------------------------

    def __str__(self) -> str:
        return f"{self.value.value}_{self.suit.value}"

    def __repr__(self) -> str:
        return self.__str__()

    # -----------------------------------------------------
    # SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "value": self.value.value,
            "suit": self.suit.value
        }

    @staticmethod
    def from_dict(data: dict) -> "Card":
        return Card(
            value=Value(data["value"]),
            suit=Suit(data["suit"])
        )

    # -----------------------------------------------------
    # HELPERS
    # -----------------------------------------------------

    def is_trump(self, trump_suit: Suit) -> bool:
        return self.suit == trump_suit


# =========================================================
# FULL 32-CARD DECK
# =========================================================

def create_deck() -> List[Card]:
    """
    Create a standard 32-card belote deck.
    """

    return [
        Card(value=value, suit=suit)
        for suit in Suit
        for value in Value
    ]


# =========================================================
# ENCODING UTILITIES
# =========================================================

CARD_INDEX = {
    str(card): idx
    for idx, card in enumerate(create_deck())
}


def card_to_index(card: Card) -> int:
    """
    Convert card to integer index.
    Useful for ML encoding.
    """

    return CARD_INDEX[str(card)]


def index_to_card(index: int) -> Card:
    """
    Convert integer index back to Card.
    """

    deck = create_deck()
    return deck[index]


# =========================================================
# ML ENCODING
# =========================================================

def hand_to_multihot(cards: List[Card]) -> List[int]:
    """
    Convert a list of cards into a 32-dimensional multi-hot vector.

    Example:
        [0,0,1,0,1,...]
    """

    vector = [0] * 32

    for card in cards:
        idx = card_to_index(card)
        vector[idx] = 1

    return vector


# =========================================================
# PARSING UTILITIES
# =========================================================

def parse_card(card_str: str) -> Card:
    """
    Parse string like:
        'AS_COEUR'
        '10_PIQUE'

    Handles extra spaces and lowercase labels.
    """

    normalized = card_str.strip().upper()

    value_str, suit_str = normalized.split("_")

    return Card(
        value=Value(value_str),
        suit=Suit(suit_str)
    )

def parse_hand(cards: List[str]) -> List[Card]:
    """
    Parse list of strings into Card objects.
    """

    return [parse_card(card) for card in cards]

def card_label_is_valid(card_str: str) -> bool:
    try:
        parse_card(card_str)
        return True
    except Exception:
        return False