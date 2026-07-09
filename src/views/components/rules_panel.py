"""
Detection rules panel.

Collects Belote rules and YOLO inference parameters.
"""

from dataclasses import dataclass

import streamlit as st

from config.settings import (
    DEFAULT_CONFIDENCE,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_IOU,
)

from src.game.belote.cards import Suit
from src.game.belote.scoring import TrumpMode


# =============================================================================
# Data model
# =============================================================================

@dataclass
class DetectionSettings:
    """Belote rules and inference settings."""

    trump_mode: TrumpMode
    trump_suit: Suit | None

    dix_de_der: bool
    belote_rebelote: bool

    confidence: float
    iou: float
    image_size: int

    deduplicate: bool


# =============================================================================
# Public API
# =============================================================================

def render_rules_panel() -> DetectionSettings:
    """
    Display Belote rules and YOLO settings.
    """

    with st.expander(
        "4. Paramètres de la manche",
        expanded=True,
    ):

        # -------------------------------------------------------------
        # Belote rules
        # -------------------------------------------------------------

        st.subheader("Règles de Belote")

        trump_mode = st.selectbox(
            "Mode de jeu",
            options=list(TrumpMode),
            format_func=lambda x: x.value,
        )

        trump_suit = None

        if trump_mode == TrumpMode.CLASSIC:

            trump_suit = st.selectbox(
                "Couleur d'atout",
                options=list(Suit),
                format_func=lambda x: x.value,
            )

        col1, col2 = st.columns(2)

        with col1:

            dix_de_der = st.checkbox(
                "Dix de Der",
                value=False,
            )

        with col2:

            belote_rebelote = st.checkbox(
                "Belote / Rebelote",
                value=True,
            )

        st.divider()

        # -------------------------------------------------------------
        # YOLO parameters
        # -------------------------------------------------------------

        st.subheader("Paramètres IA")

        confidence = st.slider(
            "Seuil de confiance",
            min_value=0.05,
            max_value=1.0,
            value=DEFAULT_CONFIDENCE,
            step=0.05,
        )

        iou = st.slider(
            "Seuil IOU",
            min_value=0.05,
            max_value=1.0,
            value=DEFAULT_IOU,
            step=0.05,
        )

        image_size = st.select_slider(
            "Taille d'image",
            options=[
                640,
                768,
                960,
                1024,
                1280,
            ],
            value=DEFAULT_IMAGE_SIZE,
        )

        deduplicate = st.checkbox(
            "Supprimer les doublons",
            value=True,
            help=(
                "Conserve uniquement la détection la plus "
                "fiable pour chaque carte."
            ),
        )

    return DetectionSettings(
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        belote_rebelote=belote_rebelote,
        confidence=confidence,
        iou=iou,
        image_size=image_size,
        deduplicate=deduplicate,
    )