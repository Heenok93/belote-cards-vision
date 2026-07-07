import streamlit as st


def load_view():

    st.title("🔮 Perspectives")

    st.markdown(
        """
        Le prototype actuel valide principalement :

        - l'expérience utilisateur,
        - la navigation Streamlit,
        - l'architecture logicielle,
        - le pipeline d'analyse.
        - la détection de cartes par un modèle YOLOv26.


        Les prochaines étapes du projet seront :
       
        - statistiques avancées.
        - choix du type de jeu: belote ou tarot.

        """
    )