"""
Database statistics repository.

Contains SQL aggregation queries used by the dashboard,
leaderboards and reporting components.
"""

from __future__ import annotations

import json

from .repositories import (
    get_connection,
    get_game,
    get_rounds,
)


# =============================================================================
# Global statistics
# =============================================================================

def get_games_count() -> int:
    """Return the total number of games."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM games
            """
        ).fetchone()

    return int(row["total"])


def get_rounds_count() -> int:
    """Return the total number of rounds."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM rounds
            """
        ).fetchone()

    return int(row["total"])


def get_detected_cards_count() -> int:
    """
    Return the total number of detected cards.

    Cards are stored as JSON arrays.
    """

    total = 0

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT cards_json
            FROM rounds
            """
        ).fetchall()

    for row in rows:

        cards = json.loads(row["cards_json"] or "[]")

        total += len(cards)

    return total


def get_average_round_score() -> float:
    """Return the average winning score."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT AVG(winning_score) AS average_score
            FROM rounds
            """
        ).fetchone()

    return float(row["average_score"] or 0)


# =============================================================================
# Current game
# =============================================================================

def get_score_totals(
    game_id: int,
) -> dict[str, int]:
    """
    Return cumulative scores for every team.

    Example
    -------
    {
        "Equipe 1": 324,
        "Equipe 2": 286
    }
    """

    totals: dict[str, int] = {}

    for row in get_rounds(game_id):

        team = row["winning_team_name"]

        totals.setdefault(team, 0)

        totals[team] += int(row["winning_score"])

    return totals


def get_current_game_summary(
    game_id: int,
) -> dict:
    """
    Return a dashboard summary for one game.
    """

    game = get_game(game_id)

    if game is None:

        return {}

    team_1 = game["team_1_name"]
    team_2 = game["team_2_name"]

    totals = get_score_totals(game_id)

    score_1 = totals.get(team_1, 0)
    score_2 = totals.get(team_2, 0)

    if score_1 > score_2:

        leader = team_1

    elif score_2 > score_1:

        leader = team_2

    else:

        leader = None

    return {

        "team_1": team_1,
        "team_2": team_2,

        "score_team_1": score_1,
        "score_team_2": score_2,

        "leader": leader,

        "difference": abs(score_1 - score_2),

        "rounds": len(get_rounds(game_id)),
    }


# =============================================================================
# Recent games
# =============================================================================

def get_recent_games(
    limit: int = 5,
) -> list[dict]:
    """
    Return the most recently updated games.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *

            FROM games

            ORDER BY updated_at DESC

            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]

def get_completed_games_count() -> int:
    """Return the number of completed games."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM games
            WHERE status='terminee'
            """
        ).fetchone()

    return int(row["total"])

def get_active_games_count() -> int:
    """Return the number of active games."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM games
            WHERE status='en_cours'
            """
        ).fetchone()

    return int(row["total"])