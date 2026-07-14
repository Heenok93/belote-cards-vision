"""
Tests for database statistics repository.
"""

from __future__ import annotations

import sqlite3

import pytest

from src.database import repositories
from src.database import statistics_repository
from src.database.schema import initialize_schema


# =============================================================================
# Statistics
# =============================================================================

def test_get_games_count(
    temporary_database,
):
    """
    The number of games should be returned.
    """

    assert statistics_repository.get_games_count() == 0

    repositories.create_game()

    assert statistics_repository.get_games_count() == 1

    repositories.create_game()

    assert statistics_repository.get_games_count() == 2

def test_get_rounds_count(
    temporary_database,
):
    """
    The number of rounds should be returned.
    """

    assert statistics_repository.get_rounds_count() == 0

    game = repositories.create_game()

    repositories.save_round(
        game_id=game,
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
    )

    assert statistics_repository.get_rounds_count() == 1

    repositories.save_round(
        game_id=game,
        winning_team_name="Equipe 2",
        winning_score=96,
        photographed_team_name="Equipe 2",
        photographed_team_won=True,
        photographed_team_score=96,
    )

    assert statistics_repository.get_rounds_count() == 2

def test_get_detected_cards_count(
    temporary_database,
):
    """
    The total number of detected cards should be returned.
    """

    assert statistics_repository.get_detected_cards_count() == 0

    game = repositories.create_game()

    repositories.save_round(
        game_id=game,
        winning_team_name="Equipe 1",
        winning_score=82,
        photographed_team_name="Equipe 1",
        photographed_team_won=True,
        photographed_team_score=82,
        cards=["AS", "KS", "QS"],
    )

    repositories.save_round(
        game_id=game,
        winning_team_name="Equipe 2",
        winning_score=96,
        photographed_team_name="Equipe 2",
        photographed_team_won=True,
        photographed_team_score=96,
        cards=["10H", "AH"],
    )

    assert statistics_repository.get_detected_cards_count() == 5

def test_get_recent_games(
    temporary_database,
):
    """
    Recent games should be returned.
    """

    first_game = repositories.create_game()

    repositories.close_game(first_game)

    second_game = repositories.create_game()

    repositories.close_game(second_game)

    recent_games = statistics_repository.get_recent_games()

    ids = {game["id"] for game in recent_games}

    assert len(recent_games) == 2

    assert first_game in ids
    assert second_game in ids

def test_get_completed_games_count(
    temporary_database,
):
    """
    The number of completed games should be returned.
    """

    assert statistics_repository.get_completed_games_count() == 0

    game = repositories.create_game()

    repositories.close_game(game)

    assert statistics_repository.get_completed_games_count() == 1

def test_get_active_games_count(
    temporary_database,
):
    """
    The number of active games should be returned.
    """

    assert statistics_repository.get_active_games_count() == 0

    repositories.create_game()

    assert statistics_repository.get_active_games_count() == 1