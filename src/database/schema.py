"""
Database schema.

Creates and migrates the SQLite database.
"""

from __future__ import annotations

import sqlite3


# =============================================================================
# Public API
# =============================================================================

def initialize_schema(connection: sqlite3.Connection) -> None:
    """
    Create or migrate the application database schema.
    """

    _create_games_table(connection)
    _create_rounds_table(connection)
    _migrate_rounds_table(connection)


# =============================================================================
# Schema creation
# =============================================================================

def _create_games_table(connection: sqlite3.Connection) -> None:
    """Create the games table."""

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS games (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            team_1_name TEXT NOT NULL DEFAULT 'Equipe 1',
            team_2_name TEXT NOT NULL DEFAULT 'Equipe 2',

            status TEXT NOT NULL DEFAULT 'en_cours',

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )


def _create_rounds_table(connection: sqlite3.Connection) -> None:
    """Create the rounds table."""

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS rounds (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            game_id INTEGER NOT NULL,

            round_number INTEGER NOT NULL,

            winning_team_name TEXT NOT NULL,
            winning_score INTEGER NOT NULL,

            photographed_team_name TEXT,
            photographed_team_won INTEGER,
            photographed_team_score INTEGER,

            raw_score INTEGER,
            corrected_score INTEGER,

            cards_json TEXT,

            trump_mode TEXT,
            trump_suit TEXT,

            dix_de_der INTEGER NOT NULL DEFAULT 0,
            belote_rebelote INTEGER NOT NULL DEFAULT 0,

            image_quality_score REAL,
            image_risk_level TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (game_id)
                REFERENCES games(id)
        )
        """
    )


# =============================================================================
# Migrations
# =============================================================================

def _migrate_rounds_table(
    connection: sqlite3.Connection,
) -> None:
    """
    Apply schema migrations on the rounds table.
    """

    existing_columns = {

        row["name"]

        for row in connection.execute(
            "PRAGMA table_info(rounds)"
        ).fetchall()

    }

    required_columns = {

        "winning_team_name":
            "TEXT",

        "winning_score":
            "INTEGER",

        "photographed_team_name":
            "TEXT",

        "photographed_team_won":
            "INTEGER",

        "photographed_team_score":
            "INTEGER",
    }

    for column_name, column_type in required_columns.items():

        if column_name in existing_columns:
            continue

        connection.execute(
            f"""
            ALTER TABLE rounds
            ADD COLUMN {column_name} {column_type}
            """
        )