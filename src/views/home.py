import streamlit as st


def load_view():

    st.title("🃏 Card Vision AI")

    st.subheader("Analyse automatisée de parties de belote")

    st.markdown(
        """
        Cette application permet d'analyser automatiquement une partie de belote
        à partir d'une photo ou d'une vidéo.

        Un modèle de Computer Vision détecte les cartes dans la main finale et l'app calcule
        automatiquement les scores associés en fonction de certains paramètres.

        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Parties analysées", "128")

    with col2:
        st.metric("Précision IA cible", "96%")

    with col3:
        st.metric("Temps moyen", "4 sec")

    st.divider()

    st.subheader("🚀 Fonctionnalités")

    st.markdown(
        """
        - Upload de vidéos et images
        - Détection des joueurs
        - Calcul automatique des scores
        - Historique des manches
        - Plus tard: choix du jeu (belote ou tarot)
        """
    )