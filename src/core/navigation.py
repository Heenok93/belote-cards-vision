"""
Navigation helpers.
"""

import streamlit as st


def redirect(page: str) -> None:
    """Redirect to another page."""

    st.query_params["page"] = page
    st.rerun()


def get_route() -> str:
    """Return the current route."""

    page = st.query_params.get("page", "home")
    return f"/{page}"