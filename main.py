"""
Card Vision AI.

Application entry point.
"""

import streamlit as st

import utils as utl

from src.core.router import render_current_page
from src.core.session import initialize_session
from src.core.navigation import redirect, get_route

from src.services.auth_service import (
    require_authentication,
    render_logout,
)
from src.services.database_service import init_db


# =============================================================================
# Streamlit configuration
# =============================================================================

st.set_page_config(
    page_title="Card Vision AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# Application initialization
# =============================================================================

initialize_session()

init_db()


# =============================================================================
# Authentication
# =============================================================================

authenticator, user = require_authentication()

render_logout(
    authenticator,
    user,
)


# =============================================================================
# Global user interface
# =============================================================================

utl.inject_custom_css()

utl.navbar_component()


# =============================================================================
# Routing
# =============================================================================

render_current_page()