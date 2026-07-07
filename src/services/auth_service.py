from pathlib import Path
import yaml
import streamlit as st
import streamlit_authenticator as stauth


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTH_CONFIG_PATH = PROJECT_ROOT / "config" / "auth_config.yaml"


def load_auth_config() -> dict:
    if not AUTH_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config auth introuvable : {AUTH_CONFIG_PATH}")

    with AUTH_CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_auth_config(config: dict) -> None:
    with AUTH_CONFIG_PATH.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config, file, sort_keys=False, allow_unicode=True)


def get_authenticator():
    config = load_auth_config()

    authenticator = stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        cookie_key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
    )

    return authenticator, config


def require_authentication():
    authenticator, config = get_authenticator()

    try:
        authenticator.login()
    except Exception as exc:
        st.error(f"Erreur d'authentification : {exc}")
        st.stop()

    authentication_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")
    username = st.session_state.get("username")

    if authentication_status is False:
        st.error("Identifiant ou mot de passe incorrect.")
        st.stop()

    if authentication_status is None:
        st.warning("Veuillez vous connecter pour accéder à l'application.")
        st.stop()

    return authenticator, {
        "name": name,
        "username": username,
    }


def render_logout(authenticator, user: dict):
    with st.sidebar:
        st.write(f"Connecté : **{user['name']}**")
        authenticator.logout("Déconnexion", "sidebar")