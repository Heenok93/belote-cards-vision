"""
Recent games component.
"""

from __future__ import annotations

import streamlit as st

from config.settings import (
    RECENT_GAMES_TITLE,
)

from src.services.database_service import (
    get_recent_games,
)


# =============================================================================
# Public API
# =============================================================================

def render_recent_games(
    limit: int = 5,
) -> None:
    """
    Display the most recent games.
    """

    games = get_recent_games(limit)

    st.subheader(RECENT_GAMES_TITLE)

    if not games:

        st.info("Aucune partie enregistrée.")

        return

    for game in games:

        status = (
            "🟢 En cours"
            if game["status"] == "en_cours"
            else "⚪ Terminée"
        )

        with st.container():

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"""
**{game["team_1_name"]}**
vs
**{game["team_2_name"]}**
"""
                )

                st.caption(status)

            with col2:

                st.caption(game["updated_at"])

            st.divider()