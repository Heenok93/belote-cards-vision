"""
Database service.

Facade over the persistence layer.
"""

from __future__ import annotations

from src.database.repositories import (
    close_game,
    create_game as repository_create_game,
    delete_round as repository_delete_round,
    get_connection,
    get_current_game as repository_get_current_game,
    get_game as repository_get_game,
    get_rounds as repository_get_rounds,
    get_score_totals as repository_get_score_totals,
    save_round,
    update_round as repository_update_round,
)

from src.database.schema import initialize_schema


# =============================================================================
# Database initialization
# =============================================================================

def init_db() -> None:
    """Initialize the application database."""

    with get_connection() as connection:
        initialize_schema(connection)


# =============================================================================
# Games
# =============================================================================

def create_game(
    team_1_name: str = "Equipe 1",
    team_2_name: str = "Equipe 2",
) -> int:
    """Create a new game."""

    return repository_create_game(
        team_1_name,
        team_2_name,
    )


def get_game(
    game_id: int,
) -> dict | None:
    """Return one game."""

    return repository_get_game(
        game_id,
    )


def get_current_game() -> dict:
    """Return the active game."""

    return repository_get_current_game()


def close_current_game(
    game_id: int,
) -> None:
    """Close the current game."""

    close_game(
        game_id,
    )


# =============================================================================
# Rounds
# =============================================================================

def save_round_score(
    **kwargs,
) -> None:
    """Persist one round."""

    save_round(
        **kwargs,
    )


def get_rounds(
    game_id: int,
) -> list[dict]:
    """Return all rounds."""

    return repository_get_rounds(
        game_id,
    )


def update_round_score(
    round_id: int,
    winning_team_name: str,
    winning_score: int,
) -> None:
    """Update one round."""

    repository_update_round(
        round_id,
        winning_team_name,
        winning_score,
    )


def delete_round(
    round_id: int,
) -> None:
    """Delete one round."""

    repository_delete_round(
        round_id,
    )


# =============================================================================
# Statistics
# =============================================================================

def get_score_totals(
    game_id: int,
) -> dict[str, int]:
    """Return cumulative scores."""

    return repository_get_score_totals(
        game_id,
    )