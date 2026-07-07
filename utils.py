import streamlit as st
from src.router import redirect


def inject_custom_css():
    with open("src/assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def navbar_component():
    with st.sidebar:
        st.title("🃏 Navigation")

        if st.button("🏠 Accueil"):
            redirect("home", reload=True)

        if st.button("📤 Upload"):
            redirect("upload", reload=True)

        if st.button("📊 Analyse"):
            redirect("analysis", reload=True)

        if st.button("🏆 Scores"):
            redirect("leaderboard", reload=True)

        if st.button("🔮 Perspectives"):
            redirect("conclusion", reload=True)