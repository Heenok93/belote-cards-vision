"""
Home page.
"""

from __future__ import annotations

import streamlit as st

from src.services.database_service import get_current_game

from src.views.components.application_statistics import (
    render_application_statistics,
)
from src.views.components.model_information import (
    render_model_information,
)
from src.views.components.recent_games import (
    render_recent_games,
)
from src.views.components.score_summary import (
    render_score_summary,
)


# =============================================================================
# Public API
# =============================================================================

def load_view() -> None:
    """Render the application home page."""

    st.title("🃏 Card Vision AI")

    st.subheader("Analyse automatisée de parties de Belote")

    st.markdown(
        """
Cette application permet d'analyser automatiquement une manche de Belote
à partir d'une photographie.

Le modèle de Computer Vision détecte les cartes, calcule automatiquement
les scores, puis permet leur validation et leur sauvegarde dans une base
de données SQLite.
"""
    )

    st.divider()

    current_game = get_current_game()

    if current_game:

        render_score_summary(
            current_game["id"],
        )

        st.divider()

    render_application_statistics()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        render_recent_games()

    with col2:

        render_model_information()

    st.divider()

    st.subheader("🚀 Fonctionnalités")

    st.markdown(
        """
- Authentification utilisateur
- Analyse automatique d'images de Belote
- Détection des cartes par Deep Learning (YOLO)
- Calcul automatique des scores
- Correction manuelle des détections
- Sauvegarde des manches
- Gestion complète des parties
- Historique et classement
"""
    )