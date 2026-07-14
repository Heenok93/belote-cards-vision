"""
Application statistics component.
"""

from __future__ import annotations

import streamlit as st

from config.settings import (
    APPLICATION_STATISTICS_TITLE,
    TOTAL_GAMES_LABEL,
    COMPLETED_GAMES_LABEL,
    ACTIVE_GAMES_LABEL,
    TOTAL_ROUNDS_LABEL,
    DETECTED_CARDS_LABEL,
    AVERAGE_SCORE_LABEL,
)

from src.services.database_service import (
    get_dashboard_statistics,
)


# =============================================================================
# Public API
# =============================================================================

def render_application_statistics() -> None:
    """
    Display global application statistics.
    """

    stats = get_dashboard_statistics()

    st.subheader(APPLICATION_STATISTICS_TITLE)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            TOTAL_GAMES_LABEL,
            stats["games"],
        )

        st.metric(
            TOTAL_ROUNDS_LABEL,
            stats["rounds"],
        )

    with col2:

        st.metric(
            COMPLETED_GAMES_LABEL,
            stats["completed_games"],
        )

        st.metric(
            DETECTED_CARDS_LABEL,
            stats["cards"],
        )

    with col3:

        st.metric(
            ACTIVE_GAMES_LABEL,
            stats["active_games"],
        )

        st.metric(
            AVERAGE_SCORE_LABEL,
            f'{stats["average_score"]:.1f} pts',
        )