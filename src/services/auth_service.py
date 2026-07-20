"""
Authentication service.

Provides authentication helpers based on streamlit-authenticator.
"""

from dataclasses import dataclass
from unicodedata import name

import streamlit as st
import streamlit_authenticator as stauth
import yaml

from config.settings import AUTH_CONFIG_PATH


# =============================================================================
# Data model
# =============================================================================

@dataclass
class AuthenticatedUser:
    """Authenticated user information."""

    name: str
    username: str


# =============================================================================
# Configuration
# =============================================================================

def load_auth_config() -> dict:
    """Load the authentication configuration."""

    if not AUTH_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config auth introuvable : {AUTH_CONFIG_PATH}"
        )

    with AUTH_CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_auth_config(config: dict) -> None:
    """Save the authentication configuration."""

    with AUTH_CONFIG_PATH.open("w", encoding="utf-8") as file:
        yaml.safe_dump(
            config,
            file,
            sort_keys=False,
            allow_unicode=True,
        )


# =============================================================================
# Authentication
# =============================================================================

def get_authenticator() -> tuple[stauth.Authenticate, dict]:
    """Create and return the Streamlit authenticator."""

    config = load_auth_config()

    authenticator = stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        cookie_key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
    )

    return authenticator, config


def _get_current_user() -> AuthenticatedUser:
    """Return the currently authenticated user."""

    name = st.session_state.get("name")
    username = st.session_state.get("username")

    assert isinstance(name, str)
    assert isinstance(username, str)

    return AuthenticatedUser(
        name=name,
        username=username,
    )

def require_authentication() -> tuple[stauth.Authenticate, AuthenticatedUser]:
    """
    Authenticate the user before accessing the application.
    """

    authenticator, _ = get_authenticator()

    try:
        authenticator.login()
    except Exception as exc:
        st.error(f"Erreur d'authentification : {exc}")
        st.stop()

    authentication_status = st.session_state.get(
        "authentication_status"
    )

    if authentication_status is False:
        st.error("Identifiant ou mot de passe incorrect.")
        st.stop()

    if authentication_status is None:
        st.warning(
            "Veuillez vous connecter pour accéder à l'application."
        )
        st.stop()

    return authenticator, _get_current_user()


# =============================================================================
# UI
# =============================================================================

def render_logout(
    authenticator: stauth.Authenticate,
    user: AuthenticatedUser,
) -> None:
    """Render the logout button in the sidebar."""

    with st.sidebar:
        st.write(f"Connecté : **{user.name}**")
        authenticator.logout("Déconnexion", "sidebar")