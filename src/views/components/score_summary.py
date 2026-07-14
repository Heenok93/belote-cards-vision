"""
Current game score summary component.
"""

from __future__ import annotations

import streamlit as st

from src.services.database_service import (
    get_current_game_summary,
)


# =============================================================================
# Public API
# =============================================================================

def render_score_summary(
    game_id: int,
) -> None:
    """
    Display the current game summary.

    Parameters
    ----------
    game_id:
        Current game identifier.
    """

    summary = get_current_game_summary(game_id)

    if not summary:

        st.info("Aucune partie active.")

        return

    st.subheader("🏆 Score actuel")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label=summary["team_1"],
            value=f'{summary["score_team_1"]} pts',
        )

    with col2:

        st.metric(
            label=summary["team_2"],
            value=f'{summary["score_team_2"]} pts',
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Leader",
            summary["leader"],
        )

    with col2:

        st.metric(
            "Écart",
            f'{summary["difference"]} pts',
        )

    with col3:

        st.metric(
            "Manches",
            summary["rounds"],
        )