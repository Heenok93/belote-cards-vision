"""
Database service.

Facade over the persistence layer.
"""

from __future__ import annotations

import sqlite3

from src.database.repositories import (
    close_game,
    create_game,
    delete_round,
    get_connection,
    get_current_game,
    get_game,
    get_rounds,
    get_score_totals,
    save_round,
    update_round,
)

from src.database.schema import initialize_schema


# =============================================================================
# Database initialization
# =============================================================================

def init_db() -> None:
    """
    Initialize the application database.
    """

    with get_connection() as connection:
        initialize_schema(connection)


# =============================================================================
# Games
# =============================================================================

def create_new_game(
    team_1_name: str = "Equipe 1",
    team_2_name: str = "Equipe 2",
) -> int:
    """
    Create a new game.
    """

    return create_game(
        team_1_name,
        team_2_name,
    )


def current_game() -> dict:
    """
    Return the active game.
    """

    return get_current_game()


def game_by_id(
    game_id: int,
) -> dict | None:
    """
    Return a game by its identifier.
    """

    return get_game(
        game_id
    )


def close_game_session(
    game_id: int,
) -> None:
    """
    Close the current game.
    """

    close_game(
        game_id
    )


# =============================================================================
# Rounds
# =============================================================================

def save_round_score(
    **kwargs,
) -> None:
    """
    Persist one round.
    """

    save_round(
        **kwargs
    )


def get_game_rounds(
    game_id: int,
) -> list[dict]:
    """
    Return every round for a game.
    """

    return get_rounds(
        game_id
    )


def update_round_score(
    round_id: int,
    winning_team_name: str,
    winning_score: int,
) -> None:
    """
    Update a round score.
    """

    update_round(
        round_id,
        winning_team_name,
        winning_score,
    )


def remove_round(
    round_id: int,
) -> None:
    """
    Delete a round.
    """

    delete_round(
        round_id
    )


# =============================================================================
# Statistics
# =============================================================================

def get_running_score(
    game_id: int,
) -> dict[str, int]:
    """
    Return cumulative scores.
    """

    return get_score_totals(
        game_id
    )