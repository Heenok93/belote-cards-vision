"""
Application session initialization.
"""

import streamlit as st


DEFAULT_SESSION = {

    # Authentication
    "authenticated": False,

    # Current game
    "game_id": None,

    # Uploaded image
    "uploaded_image": None,

    # Detection
    "analysis_result": None,
    "analysis_settings": None,
    "analysis_preprocessing": None,

    # Image quality
    "quality_report": None,

    # Manual correction
    "corrected_labels": [],
    "corrected_score_value": None,
}


def initialize_session() -> None:
    """Initialize Streamlit session state."""

    for key, value in DEFAULT_SESSION.items():
        st.session_state.setdefault(key, value)


def reset_analysis() -> None:
    """Reset the current analysis."""

    st.session_state.analysis_result = None
    st.session_state.analysis_settings = None
    st.session_state.analysis_preprocessing = None

    st.session_state.corrected_labels = []
    st.session_state.corrected_score_value = None

    st.session_state.uploaded_image = None
    st.session_state.quality_report = None