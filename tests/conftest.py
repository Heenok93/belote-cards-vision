"""
Pytest fixtures shared by all tests.
"""

from __future__ import annotations

import sqlite3

import pytest

from src.database.schema import initialize_schema
from src.database import repositories


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def connection():
    """
    Return a temporary SQLite database connection.
    """

    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    initialize_schema(connection)

    yield connection

    connection.close()

@pytest.fixture
def temporary_database(
    tmp_path,
    monkeypatch,
):
    """
    Create a temporary SQLite database for one test.
    """

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        repositories,
        "DATABASE_PATH",
        database_path,
    )

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    initialize_schema(connection)

    connection.close()

    return database_path
