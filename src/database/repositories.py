"""
Database repositories.

Provides low-level CRUD operations for the SQLite database.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from config.settings import DATABASE_PATH


# =============================================================================
# Connection
# =============================================================================

def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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
    """
    Create a new game.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

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

            VALUES (

                ?,
                ?,

                'en_cours',

                ?,
                ?

            )
            """,
            (
                team_1_name,
                team_2_name,
                now,
                now,
            ),
        )

        return cursor.lastrowid


def get_game(
    game_id: int,
) -> dict | None:
    """
    Return a game by its identifier.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *

            FROM games

            WHERE id = ?
            """,
            (
                game_id,
            ),
        ).fetchone()

    return dict(row) if row else None


def get_current_game() -> dict:
    """
    Return the currently active game.

    Creates one if none exists.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *

            FROM games

            WHERE status = 'en_cours'

            ORDER BY id DESC

            LIMIT 1
            """
        ).fetchone()

    if row:

        return dict(row)

    game_id = create_game()

    return get_game(game_id)


def close_game(
    game_id: int,
) -> None:
    """
    Close a game.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games

            SET

                status = 'terminee',

                updated_at = ?

            WHERE id = ?
            """,
            (
                now,
                game_id,
            ),
        )


def update_game_timestamp(
    game_id: int,
) -> None:
    """
    Refresh the update timestamp.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games

            SET updated_at = ?

            WHERE id = ?
            """,
            (
                now,
                game_id,
            ),
        )

"""
Database repositories.

Provides low-level CRUD operations for the SQLite database.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from config.settings import DATABASE_PATH


# =============================================================================
# Connection
# =============================================================================

def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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
    """
    Create a new game.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

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

            VALUES (

                ?,
                ?,

                'en_cours',

                ?,
                ?

            )
            """,
            (
                team_1_name,
                team_2_name,
                now,
                now,
            ),
        )

        return cursor.lastrowid


def get_game(
    game_id: int,
) -> dict | None:
    """
    Return a game by its identifier.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *

            FROM games

            WHERE id = ?
            """,
            (
                game_id,
            ),
        ).fetchone()

    return dict(row) if row else None


def get_current_game() -> dict:
    """
    Return the currently active game.

    Creates one if none exists.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *

            FROM games

            WHERE status = 'en_cours'

            ORDER BY id DESC

            LIMIT 1
            """
        ).fetchone()

    if row:

        return dict(row)

    game_id = create_game()

    return get_game(game_id)


def close_game(
    game_id: int,
) -> None:
    """
    Close a game.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games

            SET

                status = 'terminee',

                updated_at = ?

            WHERE id = ?
            """,
            (
                now,
                game_id,
            ),
        )


def update_game_timestamp(
    game_id: int,
) -> None:
    """
    Refresh the update timestamp.
    """

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE games

            SET updated_at = ?

            WHERE id = ?
            """,
            (
                now,
                game_id,
            ),
        )