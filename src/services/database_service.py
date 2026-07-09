import json
import sqlite3
from datetime import datetime

from config.settings import DATABASE_PATH

def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
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

        conn.execute(
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
                FOREIGN KEY (game_id) REFERENCES games(id)
            )
            """
        )

        migrate_rounds_table(conn)


def migrate_rounds_table(conn):
    existing_columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(rounds)").fetchall()
    }

    required_columns = {
        "winning_team_name": "TEXT",
        "winning_score": "INTEGER",
        "photographed_team_name": "TEXT",
        "photographed_team_won": "INTEGER",
        "photographed_team_score": "INTEGER",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            conn.execute(
                f"ALTER TABLE rounds ADD COLUMN {column_name} {column_type}"
            )


def create_game(
    team_1_name: str = "Equipe 1",
    team_2_name: str = "Equipe 2",
) -> int:
    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.execute(
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
            (team_1_name, team_2_name, now, now),
        )

        return cursor.lastrowid


def get_game(game_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM games
            WHERE id = ?
            """,
            (game_id,),
        ).fetchone()

    return dict(row) if row else None


def get_current_game():
    with get_connection() as conn:
        game = conn.execute(
            """
            SELECT *
            FROM games
            WHERE status = 'en_cours'
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if game is not None:
        return dict(game)

    game_id = create_game()
    return get_game(game_id)


def get_next_round_number(game_id: int):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COALESCE(MAX(round_number), 0) + 1 AS next_round
            FROM rounds
            WHERE game_id = ?
            """,
            (game_id,),
        ).fetchone()

    return int(row["next_round"])


def save_round_score(
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
):
    now = datetime.now().isoformat(timespec="seconds")
    round_number = get_next_round_number(game_id)

    with get_connection() as conn:
        conn.execute(
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

        conn.execute(
            """
            UPDATE games
            SET updated_at = ?
            WHERE id = ?
            """,
            (now, game_id),
        )


def get_rounds(game_id: int):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM rounds
            WHERE game_id = ?
            ORDER BY round_number ASC, id ASC
            """,
            (game_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_score_totals(game_id: int):
    rounds = get_rounds(game_id)

    totals = {
        "Equipe 1": 0,
        "Equipe 2": 0,
    }

    for row in rounds:
        team = row.get("winning_team_name")
        score = row.get("winning_score")

        if team is not None and score is not None:
            totals[team] = totals.get(team, 0) + int(score)

    return totals


def update_round_score(
    round_id: int,
    winning_team_name: str,
    winning_score: int,
):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE rounds
            SET winning_team_name = ?,
                winning_score = ?
            WHERE id = ?
            """,
            (winning_team_name, winning_score, round_id),
        )


def delete_round(round_id: int):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM rounds
            WHERE id = ?
            """,
            (round_id,),
        )


def close_current_game(game_id: int):
    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE games
            SET status = 'terminee',
                updated_at = ?
            WHERE id = ?
            """,
            (now, game_id),
        )