"""
Application session initialization.
"""

import streamlit as st


DEFAULT_SESSION = {

    # Navigation
    "current_page": "home",

    # Authentication
    "authenticated": False,

    # Current game
    "game_id": None,

    # Uploaded image
    "uploaded_image": None,

    # Detection results
    "analysis_result": None,

    # Corrected cards
    "corrected_cards": [],

    # UI state
    "image_quality": None,

    # Leaderboard
    "score_totals": None,
}


def initialize_session() -> None:
    """Initialize Streamlit session state."""

    for key, value in DEFAULT_SESSION.items():
        st.session_state.setdefault(key, value)


def reset_analysis() -> None:
    """Reset analysis-related session values."""

    st.session_state.analysis_result = None
    st.session_state.corrected_cards = []
    st.session_state.uploaded_image = None
    st.session_state.image_quality = None