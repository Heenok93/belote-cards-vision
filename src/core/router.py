"""
Application router.

Resolves the current route and renders the corresponding page.
"""

from collections.abc import Callable

import streamlit as st

from src.core.navigation import get_route

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
    "/home": home.load_view,
    "/upload": upload.load_view,
    "/analysis": game_analysis.load_view,
    "/leaderboard": leaderboard.load_view,
    "/conclusion": conclusion.load_view,
}

# =============================================================================
# Public API
# =============================================================================

def render_current_page() -> None:
    """Render the page matching the current route."""

    route = get_route()

    page = ROUTES.get(
        route,
        home.load_view,
    )

    page()