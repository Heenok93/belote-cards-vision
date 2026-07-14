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
    save_round,
    update_round as repository_update_round,
)

from src.database.schema import initialize_schema

from src.database.statistics_repository import (
    get_average_round_score as repository_get_average_round_score,
    get_completed_games_count as repository_get_completed_games_count,
    get_current_game_summary as repository_get_current_game_summary,
    get_detected_cards_count as repository_get_detected_cards_count,
    get_games_count as repository_get_games_count,
    get_recent_games as repository_get_recent_games,
    get_rounds_count as repository_get_rounds_count,
    get_score_totals as repository_get_score_totals,
    get_active_games_count as repository_get_active_games_count,
)


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

def get_games_count() -> int:
    """Return the total number of games."""

    return repository_get_games_count()


def get_completed_games_count() -> int:
    """Return the number of completed games."""

    return repository_get_completed_games_count()


def get_active_games_count() -> int:
    """Return the number of active games."""

    return repository_get_active_games_count()


def get_rounds_count() -> int:
    """Return the total number of rounds."""

    return repository_get_rounds_count()


def get_detected_cards_count() -> int:
    """Return the total number of detected cards."""

    return repository_get_detected_cards_count()


def get_average_round_score() -> float:
    """Return the average winning score."""

    return repository_get_average_round_score()


def get_recent_games(
    limit: int = 5,
) -> list[dict]:
    """Return the most recent games."""

    return repository_get_recent_games(
        limit,
    )


def get_current_game_summary(
    game_id: int,
) -> dict:
    """Return dashboard information for one game."""

    return repository_get_current_game_summary(
        game_id,
    )


def get_score_totals(
    game_id: int,
) -> dict[str, int]:
    """Return cumulative scores."""

    return repository_get_score_totals(
        game_id,
    )

def get_dashboard_statistics() -> dict:
    """
    Return global statistics displayed on the dashboard.
    """

    return {
        "games": get_games_count(),
        "completed_games": get_completed_games_count(),
        "active_games": get_active_games_count(),
        "rounds": get_rounds_count(),
        "cards": get_detected_cards_count(),
        "average_score": get_average_round_score(),
    }