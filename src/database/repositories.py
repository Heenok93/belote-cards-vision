"""
Database repositories.

Low-level CRUD operations for the SQLite database.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from config.settings import DATABASE_PATH
from src import game


# =============================================================================
# Connection
# =============================================================================

def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# =============================================================================
# Games
# =============================================================================

def create_game(
    team_1_name: str = "Equipe 1",
    team_2_name: str = "Equipe 2",
) -> int:
    """Create a new game."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO games (
                team_1_name,
                team_2_name,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, 'en_cours', ?, ?)
            """,
            (
                team_1_name,
                team_2_name,
                now,
                now,
            ),
        )

        assert cursor.lastrowid is not None
        return cursor.lastrowid 


def get_game(game_id: int) -> dict | None:
    """Return one game."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM games
            WHERE id = ?
            """,
            (game_id,),
        ).fetchone()

    return dict(row) if row else None


def get_current_game() -> dict:
    """Return the active game. Creates one if needed."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM games
            WHERE status='en_cours'
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if row:
        return dict(row)

    game_id = create_game()

    game = get_game(game_id)
    assert game is not None

    return game


def close_game(game_id: int) -> None:
    """Close a game."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games
            SET
                status='terminee',
                updated_at=?
            WHERE id=?
            """,
            (
                now,
                game_id,
            ),
        )


def update_game_timestamp(game_id: int) -> None:
    """Refresh updated_at."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games
            SET updated_at=?
            WHERE id=?
            """,
            (
                now,
                game_id,
            ),
        )


# =============================================================================
# Rounds
# =============================================================================

def get_next_round_number(
    connection: sqlite3.Connection,
    game_id: int,
) -> int:
    """Return the next round number."""

    row = connection.execute(
        """
        SELECT
            COALESCE(MAX(round_number),0)+1 AS next_round
        FROM rounds
        WHERE game_id=?
        """,
        (game_id,),
    ).fetchone()

    return int(row["next_round"])


def save_round(
    *,
    game_id: int,
    winning_team_name: str,
    winning_score: int,
    photographed_team_name: str,
    photographed_team_won: bool,
    photographed_team_score: int,
    raw_score: int | None = None,
    corrected_score: int | None = None,
    cards: list[str] | None = None,
    trump_mode: str | None = None,
    trump_suit: str | None = None,
    dix_de_der: bool = False,
    belote_rebelote: bool = False,
    image_quality_score: float | None = None,
    image_risk_level: str | None = None,
) -> None:
    """Save one round."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        round_number = get_next_round_number(
            connection,
            game_id,
        )

        connection.execute(
            """
            INSERT INTO rounds (

                game_id,
                round_number,

                winning_team_name,
                winning_score,

                photographed_team_name,
                photographed_team_won,
                photographed_team_score,

                raw_score,
                corrected_score,

                cards_json,

                trump_mode,
                trump_suit,

                dix_de_der,
                belote_rebelote,

                image_quality_score,
                image_risk_level,

                created_at

            )

            VALUES (

                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?

            )
            """,
            (
                game_id,
                round_number,

                winning_team_name,
                winning_score,

                photographed_team_name,
                int(photographed_team_won),
                photographed_team_score,

                raw_score,
                corrected_score,

                json.dumps(cards or [], ensure_ascii=False),

                trump_mode,
                trump_suit,

                int(dix_de_der),
                int(belote_rebelote),

                image_quality_score,
                image_risk_level,

                now,
            ),
        )

    update_game_timestamp(game_id)


def get_rounds(
    game_id: int,
) -> list[dict]:
    """Return all rounds."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM rounds
            WHERE game_id=?
            ORDER BY round_number,id
            """,
            (game_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def update_round(
    round_id: int,
    winning_team_name: str,
    winning_score: int,
) -> None:
    """Update one round."""

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE rounds
            SET
                winning_team_name=?,
                winning_score=?
            WHERE id=?
            """,
            (
                winning_team_name,
                winning_score,
                round_id,
            ),
        )


def delete_round(
    round_id: int,
) -> None:
    """Delete one round."""

    with get_connection() as connection:

        connection.execute(
            """
            DELETE FROM rounds
            WHERE id=?
            """,
            (round_id,),
        )
