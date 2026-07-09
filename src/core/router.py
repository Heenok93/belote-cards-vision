"""
Application router.

Centralise la navigation entre les différentes pages Streamlit.
"""

from collections.abc import Callable

import streamlit as st

from src.views.pages import (
    conclusion,
    game_analysis,
    home,
    leaderboard,
    upload,
)

# =============================================================================
# Route registry
# =============================================================================

ROUTES: dict[str, Callable[[], None]] = {
    "home": home.load_view,
    "upload": upload.load_view,
    "analysis": game_analysis.load_view,
    "leaderboard": leaderboard.load_view,
    "conclusion": conclusion.load_view,
}


# =============================================================================
# Navigation
# =============================================================================

def navigate(page: str) -> None:
    """Navigate to another page."""

    if page not in ROUTES:
        raise ValueError(f"Unknown route: {page}")

    st.session_state.current_page = page


def current_page() -> str:
    """Return the current page."""

    return st.session_state.get("current_page", "home")


def render_current_page() -> None:
    """Render the current page."""

    page = current_page()

    ROUTES.get(page, home.load_view)()