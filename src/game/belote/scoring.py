from enum import Enum
from typing import List

from .cards import Card, Suit, Value
from .constants import (
    NON_TRUMP_POINTS,
    TRUMP_POINTS,
    DIX_DE_DER_BONUS,
    BELOTE_REBELOTE_BONUS,
    BASE_TOTAL_POINTS,
)


# =========================================================
# TRUMP MODES
# =========================================================

class TrumpMode(Enum):
    CLASSIC = "CLASSIC"
    ALL_TRUMP = "ALL_TRUMP"
    NO_TRUMP = "NO_TRUMP"


# =========================================================
# CARD SCORING
# =========================================================

def get_card_points(
    card: Card,
    trump_mode: TrumpMode = TrumpMode.CLASSIC,
    trump_suit: Suit | None = None,
) -> int:
    """
    Return the number of points for a single card.

    Rules
    -----
    CLASSIC:
        Only cards of trump_suit use the trump point table.

    ALL_TRUMP:
        All cards use the trump point table.

    NO_TRUMP:
        All cards use the non-trump point table.
    """

    if trump_mode == TrumpMode.ALL_TRUMP:
        return TRUMP_POINTS[card.value]

    if trump_mode == TrumpMode.NO_TRUMP:
        return NON_TRUMP_POINTS[card.value]

    if trump_mode == TrumpMode.CLASSIC:
        if trump_suit is None:
            raise ValueError("trump_suit is required in CLASSIC mode.")

        if card.suit == trump_suit:
            return TRUMP_POINTS[card.value]

        return NON_TRUMP_POINTS[card.value]

    raise ValueError(f"Unknown trump mode: {trump_mode}")


# =========================================================
# BONUS DETECTION
# =========================================================

def has_belote_rebelote(
    cards: List[Card],
    trump_mode: TrumpMode = TrumpMode.CLASSIC,
    trump_suit: Suit | None = None,
) -> bool:
    """
    Detect belote/rebelote.

    Belote/rebelote only exists in CLASSIC mode.

    Condition:
        - King of trump
        - Queen of trump
    """

    if trump_mode != TrumpMode.CLASSIC:
        return False

    if trump_suit is None:
        return False

    king_of_trump = Card(Value.ROI, trump_suit)
    queen_of_trump = Card(Value.DAME, trump_suit)

    return (
        king_of_trump in cards
        and queen_of_trump in cards
    )


# =========================================================
# SCORE COMPUTATION
# =========================================================

def compute_score(
    cards: List[Card],
    trump_mode: TrumpMode = TrumpMode.CLASSIC,
    trump_suit: Suit | None = None,
    dix_de_der: bool = False,
    include_belote_rebelote: bool = True,
) -> int:
    """
    Compute the total belote score for a list of cards.

    Parameters
    ----------
    cards : List[Card]
        Cards to score.

    trump_mode : TrumpMode
        Scoring mode:
            - CLASSIC
            - ALL_TRUMP
            - NO_TRUMP

    trump_suit : Suit | None
        Trump suit in CLASSIC mode.
        Ignored in ALL_TRUMP and NO_TRUMP modes.

    dix_de_der : bool
        Add 10 bonus points if True.

    include_belote_rebelote : bool
        Enable automatic belote/rebelote detection.
        Only applies in CLASSIC mode.

    Returns
    -------
    int
        Total score.
    """

    score = 0

    for card in cards:
        score += get_card_points(
            card=card,
            trump_mode=trump_mode,
            trump_suit=trump_suit,
        )

    if dix_de_der:
        score += DIX_DE_DER_BONUS

    if include_belote_rebelote:
        if has_belote_rebelote(
            cards=cards,
            trump_mode=trump_mode,
            trump_suit=trump_suit,
        ):
            score += BELOTE_REBELOTE_BONUS

    return score


# =========================================================
# VALIDATION UTILITIES
# =========================================================

def validate_total_score(
    total_score: int,
    trump_mode: TrumpMode = TrumpMode.CLASSIC,
    dix_de_der: bool = False,
    belote_rebelote: bool = False,
) -> bool:
    """
    Validate that a full game total is coherent.

    Base totals
    -----------
    CLASSIC:
        162 points

    ALL_TRUMP:
        Uses trump point table for every suit.

    NO_TRUMP:
        Uses non-trump point table for every suit.

    Bonuses
    -------
    dix_de_der:
        +10 points

    belote/rebelote:
        +20 points, CLASSIC mode only.
    """

    if trump_mode == TrumpMode.CLASSIC:
        expected_score = BASE_TOTAL_POINTS

    elif trump_mode == TrumpMode.ALL_TRUMP:
        expected_score = sum(
            TRUMP_POINTS[value] * 4
            for value in Value
        )

    elif trump_mode == TrumpMode.NO_TRUMP:
        expected_score = sum(
            NON_TRUMP_POINTS[value] * 4
            for value in Value
        )

    else:
        raise ValueError(f"Unknown trump mode: {trump_mode}")

    if dix_de_der:
        expected_score += DIX_DE_DER_BONUS

    if trump_mode == TrumpMode.CLASSIC and belote_rebelote:
        expected_score += BELOTE_REBELOTE_BONUS

    return total_score == expected_score


# =========================================================
# TEAM SCORE
# =========================================================

def compute_team_scores(
    team_1_cards: List[Card],
    team_2_cards: List[Card],
    trump_mode: TrumpMode = TrumpMode.CLASSIC,
    trump_suit: Suit | None = None,
    team_1_dix_de_der: bool = False,
    team_2_dix_de_der: bool = False,
    include_belote_rebelote: bool = True,
) -> dict:
    """
    Compute both team scores.

    Parameters
    ----------
    team_1_cards : List[Card]
        Cards won by team 1.

    team_2_cards : List[Card]
        Cards won by team 2.

    trump_mode : TrumpMode
        CLASSIC, ALL_TRUMP, or NO_TRUMP.

    trump_suit : Suit | None
        Required only for CLASSIC mode.

    team_1_dix_de_der : bool
        Whether team 1 won the last trick.

    team_2_dix_de_der : bool
        Whether team 2 won the last trick.

    include_belote_rebelote : bool
        Enable belote/rebelote automatic bonus in CLASSIC mode.

    Returns
    -------
    dict
        {
            "team_1": int,
            "team_2": int
        }
    """

    team_1_score = compute_score(
        cards=team_1_cards,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=team_1_dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )

    team_2_score = compute_score(
        cards=team_2_cards,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=team_2_dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )

    return {
        "team_1": team_1_score,
        "team_2": team_2_score,
    }


# =========================================================
# DEBUG / EXAMPLE
# =========================================================

if __name__ == "__main__":

    example_hand = [
        Card(Value.AS, Suit.COEUR),
        Card(Value.DIX, Suit.COEUR),
        Card(Value.ROI, Suit.COEUR),
        Card(Value.DAME, Suit.COEUR),
        Card(Value.VALET, Suit.COEUR),
    ]

    score_classic = compute_score(
        cards=example_hand,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
        dix_de_der=True,
    )

    score_all_trump = compute_score(
        cards=example_hand,
        trump_mode=TrumpMode.ALL_TRUMP,
        dix_de_der=True,
    )

    score_no_trump = compute_score(
        cards=example_hand,
        trump_mode=TrumpMode.NO_TRUMP,
        dix_de_der=True,
    )

    print("Classic score:", score_classic)
    print("All trump score:", score_all_trump)
    print("No trump score:", score_no_trump)