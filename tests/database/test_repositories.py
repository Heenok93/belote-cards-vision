"""
Tests for database repositories.
"""

from __future__ import annotations



from src.database import repositories


# =============================================================================
# Games
# =============================================================================

def test_create_game(
    temporary_database,
):
    """
    A newly created game should be persisted.
    """

    game_id = repositories.create_game()

    game = repositories.get_game(game_id)

    assert game is not None
    assert game["id"] == game_id
    assert game["team_1_name"] == "Equipe 1"
    assert game["team_2_name"] == "Equipe 2"
    assert game["status"] == "en_cours"


def test_get_current_game_returns_same_game(
    temporary_database,
):
    """
    The current game should be created only once.
    """

    first_game = repositories.get_current_game()

    second_game = repositories.get_current_game()

    assert first_game["id"] == second_game["id"]
    assert first_game["status"] == "en_cours"

def test_save_round(
    temporary_database,
):
    """
    A saved round should be persisted.
    """

    game = repositories.get_current_game()

    repositories.save_round(
        game_id=game["id"],
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
        raw_score=80,
        corrected_score=82,
        cards=["AS", "10S", "KH"],
        trump_mode="normal",
        trump_suit="S",
        dix_de_der=True,
        belote_rebelote=False,
        image_quality_score=0.95,
        image_risk_level="Faible",
    )

    rounds = repositories.get_rounds(game["id"])

    assert len(rounds) == 1

    round_ = rounds[0]

    assert round_["round_number"] == 1
    assert round_["winning_team_name"] == "Equipe 1"
    assert round_["winning_score"] == 82

def test_update_round(
    temporary_database,
):
    """
    A round should be updated.
    """

    game = repositories.get_current_game()

    repositories.save_round(
        game_id=game["id"],
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
    )

    round_id = repositories.get_rounds(game["id"])[0]["id"]

    repositories.update_round(
        round_id,
        "Equipe 2",
        96,
    )

    updated_round = repositories.get_rounds(game["id"])[0]

    assert updated_round["winning_team_name"] == "Equipe 2"
    assert updated_round["winning_score"] == 96

def test_delete_round(
    temporary_database,
):
    """
    A round should be deleted.
    """

    game = repositories.get_current_game()

    repositories.save_round(
        game_id=game["id"],
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
    )

    round_id = repositories.get_rounds(game["id"])[0]["id"]

    repositories.delete_round(round_id)

    rounds = repositories.get_rounds(game["id"])

    assert rounds == []

def test_close_game(
    temporary_database,
):
    """
    A game should be marked as completed.
    """

    game = repositories.get_current_game()

    repositories.close_game(game["id"])

    updated_game = repositories.get_game(game["id"])

    assert updated_game["status"] == "terminee"