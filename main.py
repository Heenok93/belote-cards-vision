import streamlit as st

from src.views import (
    home,
    upload,
    game_analysis,
    leaderboard,
    conclusion,
)

from src.router import get_route
import utils as utl

from src.services.auth_service import require_authentication, render_logout
from src.services.database_service import init_db


st.set_page_config(
    layout="wide",
    page_title="Card Vision AI",
    initial_sidebar_state="expanded",
)

init_db()

authenticator, user = require_authentication()
render_logout(authenticator, user)

utl.inject_custom_css()
utl.navbar_component()


def navigation():
    route = get_route()

    if route == "/home":
        home.load_view()

    elif route == "/upload":
        upload.load_view()

    elif route == "/analysis":
        game_analysis.load_view()

    elif route == "/leaderboard":
        leaderboard.load_view()

    elif route == "/conclusion":
        conclusion.load_view()

    else:
        home.load_view()


navigation()