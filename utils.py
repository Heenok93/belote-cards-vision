from pathlib import Path

import streamlit as st


# =============================================================================
# CSS
# =============================================================================

def inject_custom_css() -> None:
    """Load the application stylesheet."""

    css_path = Path("src/assets/styles.css")

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


# =============================================================================
# Navigation
# =============================================================================

def navbar_component() -> None:
    """Render the application sidebar."""

    with st.sidebar:

        st.title("🃏 Navigation")

        if st.button("🏠 Accueil", use_container_width=True):
            st.query_params["page"] = "home"
            st.rerun()

        if st.button("📤 Upload", use_container_width=True):
            st.query_params["page"] = "upload"
            st.rerun()

        if st.button("📊 Analyse", use_container_width=True):
            st.query_params["page"] = "analysis"
            st.rerun()

        if st.button("🏆 Scores", use_container_width=True):
            st.query_params["page"] = "leaderboard"
            st.rerun()

        if st.button("🔮 Perspectives", use_container_width=True):
            st.query_params["page"] = "conclusion"
            st.rerun()


def get_route() -> str:
    """Return the current route."""

    page = st.query_params.get("page", "home")

    return f"/{page}"