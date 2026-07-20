"""
Tests for database service.
"""

from __future__ import annotations



from src.services import database_service

def test_create_game(
    temporary_database,
):
    """
    A game should be created through the service.
    """

    game_id = database_service.create_game()

    game = database_service.get_game(game_id)

    assert game is not None
    assert game["id"] == game_id

def test_get_current_game(
    temporary_database,
):
    """
    The current game should be returned.
    """

    game = database_service.get_current_game()

    assert game["status"] == "en_cours"

    same_game = database_service.get_current_game()

    assert same_game["id"] == game["id"]

def test_save_round_score(
    temporary_database,
):
    """
    A round should be saved through the service.
    """

    game = database_service.get_current_game()

    database_service.save_round_score(
        game_id=game["id"],
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
    )

    rounds = database_service.get_rounds(game["id"])

    assert len(rounds) == 1

def test_get_score_totals(
    temporary_database,
):
    """
    Score totals should be computed.
    """

    game = database_service.get_current_game()

    database_service.save_round_score(
        game_id=game["id"],
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
    )

    totals = database_service.get_score_totals(game["id"])

    assert totals["Equipe 1"] == 82

def test_close_current_game(
    temporary_database,
):
    """
    A game should be closed through the service.
    """

    game = database_service.get_current_game()

    database_service.close_current_game(game["id"])

    updated_game = database_service.get_game(game["id"])

    assert updated_game["status"] == "terminee"