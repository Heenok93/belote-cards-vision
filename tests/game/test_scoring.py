import pytest

from src.game.belote.cards import Card, Suit, Value
from src.game.belote.scoring import (
    TrumpMode,
    compute_score,
    compute_team_scores,
    get_card_points,
    has_belote_rebelote,
    validate_total_score,
)

def test_get_card_points_classic():
    """
    Trump cards should use the trump scoring table.
    """

    card = Card(
        Value.VALET,
        Suit.COEUR,
    )

    score = get_card_points(
        card=card,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
    )

    assert score == 20

def test_get_card_points_non_trump():
    """
    Non-trump cards should use the normal scoring table.
    """

    card = Card(
        Value.VALET,
        Suit.PIQUE,
    )

    score = get_card_points(
        card=card,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
    )

    assert score == 2

def test_has_belote_rebelote():
    """
    King and Queen of trump should trigger Belote/Rebelote.
    """

    cards = [
        Card(Value.ROI, Suit.COEUR),
        Card(Value.DAME, Suit.COEUR),
    ]

    assert has_belote_rebelote(
        cards,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
    )

def test_compute_score_with_dix_de_der():
    """
    Dix de Der bonus should be added.
    """

    cards = [
        Card(Value.AS, Suit.COEUR),
    ]

    score = compute_score(
        cards,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.PIQUE,
        dix_de_der=True,
    )

    assert score == 21

def test_compute_score_with_belote_rebelote():
    """
    Belote/Rebelote bonus should be added automatically.
    """

    cards = [
        Card(Value.ROI, Suit.COEUR),
        Card(Value.DAME, Suit.COEUR),
    ]

    score = compute_score(
        cards=cards,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
    )

    # Roi (4) + Dame (3) + Belote (20)
    assert score == 27



def test_validate_total_score():
    """
    A complete classic game should total 162 points.
    """

    assert validate_total_score(
        total_score=162,
        trump_mode=TrumpMode.CLASSIC,
    )

    assert not validate_total_score(
        total_score=161,
        trump_mode=TrumpMode.CLASSIC,
    )



def test_compute_team_scores():
    """
    Team scores should be computed independently.
    """

    team_1_cards = [
        Card(Value.AS, Suit.COEUR),
    ]

    team_2_cards = [
        Card(Value.DIX, Suit.PIQUE),
    ]

    scores = compute_team_scores(
        team_1_cards=team_1_cards,
        team_2_cards=team_2_cards,
        trump_mode=TrumpMode.CLASSIC,
        trump_suit=Suit.COEUR,
    )

    assert scores["team_1"] == 11
    assert scores["team_2"] == 10

def test_get_card_points_requires_trump_suit():
    """
    Classic mode requires a trump suit.
    """

    card = Card(
        Value.AS,
        Suit.COEUR,
    )

    with pytest.raises(ValueError):

        get_card_points(
            card=card,
            trump_mode=TrumpMode.CLASSIC,
        )