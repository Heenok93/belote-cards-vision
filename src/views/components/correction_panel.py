"""
Correction panel.

Provides manual correction tools after YOLO inference.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.game.belote.cards import Suit, parse_card
from src.game.belote.scoring import TrumpMode, compute_score


# =============================================================================
# Constants
# =============================================================================

ALL_CARD_LABELS = [
    "7_TREFLE", "7_CARREAU", "7_COEUR", "7_PIQUE",
    "8_TREFLE", "8_CARREAU", "8_COEUR", "8_PIQUE",
    "9_TREFLE", "9_CARREAU", "9_COEUR", "9_PIQUE",
    "10_TREFLE", "10_CARREAU", "10_COEUR", "10_PIQUE",
    "VALET_TREFLE", "VALET_CARREAU", "VALET_COEUR", "VALET_PIQUE",
    "DAME_TREFLE", "DAME_CARREAU", "DAME_COEUR", "DAME_PIQUE",
    "ROI_TREFLE", "ROI_CARREAU", "ROI_COEUR", "ROI_PIQUE",
    "AS_TREFLE", "AS_CARREAU", "AS_COEUR", "AS_PIQUE",
]


# =============================================================================
# Helpers
# =============================================================================

def get_score_value(score):
    """Return a numeric score."""

    if hasattr(score, "total"):
        return score.total

    return score


def deduplicate_labels(labels: list[str]) -> list[str]:
    """Remove duplicate labels while preserving order."""

    return list(dict.fromkeys(labels))


def validate_card_count(n_cards: int) -> None:
    """Validate the number of cards."""

    if n_cards == 0:

        st.warning(
            "Aucune carte retenue pour le score final."
        )

    elif n_cards > 32:

        st.error(
            "Plus de 32 cartes retenues : impossible pour une partie de Belote."
        )

    elif n_cards % 4 != 0:

        st.warning(
            "Nombre de cartes suspect : le total devrait être un multiple "
            "de 4 (4, 8, 12, ..., 32)."
        )

    else:

        st.success(
            "Nombre de cartes cohérent avec une distribution de Belote."
        )


def compute_corrected_score(
    labels: list[str],
    trump_mode: TrumpMode,
    trump_suit: Suit | None,
    dix_de_der: bool,
    include_belote_rebelote: bool,
):
    """Compute the corrected Belote score."""

    cards = [
        parse_card(label)
        for label in labels
    ]

    return compute_score(
        cards=cards,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )


# =============================================================================
# Mobile correction
# =============================================================================

def render_mobile_correction(
    detections: list[dict],
) -> list[str]:
    """Render the mobile-friendly correction interface."""

    corrected_labels: list[str] = []

    for i, detection in enumerate(detections):

        label = detection["label"]
        confidence = round(
            detection["confidence"],
            3,
        )

        st.markdown(
            f"**Carte {i + 1} — {label}**"
        )

        st.caption(
            f"Confiance IA : {confidence}"
        )

        keep = st.checkbox(
            "Garder cette carte",
            value=True,
            key=f"keep_card_{i}",
        )

        default_label = (
            label
            if label in ALL_CARD_LABELS
            else ALL_CARD_LABELS[0]
        )

        corrected_label = st.selectbox(
            "Carte corrigée",
            options=ALL_CARD_LABELS,
            index=ALL_CARD_LABELS.index(
                default_label
            ),
            key=f"corrected_card_{i}",
        )

        if keep:
            corrected_labels.append(
                corrected_label
            )

        st.divider()

    return corrected_labels


# =============================================================================
# Advanced table correction
# =============================================================================

def render_table_correction(
    detections: list[dict],
) -> list[str]:
    """Render the advanced correction table."""

    rows = []

    for detection in detections:

        rows.append(
            {
                "Garder": True,
                "Carte détectée": detection["label"],
                "Carte corrigée": (
                    detection["label"]
                    if detection["valid"]
                    else ALL_CARD_LABELS[0]
                ),
                "Confiance": round(
                    detection["confidence"],
                    3,
                ),
            }
        )

    dataframe = pd.DataFrame(rows)

    edited = st.data_editor(
        dataframe,
        use_container_width=True,
        hide_index=True,
        key="card_correction_editor",
        column_config={

            "Garder":
                st.column_config.CheckboxColumn(
                    "Garder",
                    help=(
                        "Décoche pour supprimer "
                        "une fausse détection."
                    ),
                ),

            "Carte détectée":
                st.column_config.TextColumn(
                    "Carte détectée",
                    disabled=True,
                ),

            "Carte corrigée":
                st.column_config.SelectboxColumn(
                    "Carte corrigée",
                    options=ALL_CARD_LABELS,
                ),

            "Confiance":
                st.column_config.NumberColumn(
                    "Confiance",
                    disabled=True,
                    format="%.3f",
                ),
        },
    )

    return edited.loc[
        edited["Garder"],
        "Carte corrigée",
    ].tolist()

# =============================================================================
# Public API
# =============================================================================

def render_correction_panel(
    result: dict,
    trump_mode: TrumpMode,
    trump_suit: Suit | None,
    dix_de_der: bool,
    include_belote_rebelote: bool,
):
    """
    Display the manual correction workflow.

    Returns
    -------
    dict | None
        Dictionary containing the corrected labels and score.
    """

    detections = result["detections"]

    if not detections:

        st.warning(
            "Aucune carte détectée. Essaie de baisser le seuil de confiance "
            "ou d'utiliser une photo plus nette."
        )

        return None

    correction_mode = st.radio(
        "Mode de correction",
        [
            "Correction simple",
            "Tableau avancé",
        ],
        horizontal=False,
    )

    if correction_mode == "Correction simple":

        corrected_labels = render_mobile_correction(
            detections
        )

    else:

        corrected_labels = render_table_correction(
            detections
        )

    # ------------------------------------------------------------------
    # Add missing cards
    # ------------------------------------------------------------------

    with st.expander(
        "Ajouter des cartes manquantes",
        expanded=False,
    ):

        added_cards = st.multiselect(
            "Cartes à ajouter",
            options=ALL_CARD_LABELS,
            default=[],
        )

        corrected_labels.extend(
            added_cards
        )

    corrected_labels = deduplicate_labels(
        corrected_labels
    )

    corrected_score = compute_corrected_score(
        labels=corrected_labels,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )

    corrected_score_value = get_score_value(
        corrected_score
    )

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    st.session_state.corrected_labels = (
        corrected_labels
    )

    st.session_state.corrected_score_value = (
        corrected_score_value
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    st.subheader(
        "Score final corrigé"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Score corrigé",
            corrected_score_value,
        )

    with col2:

        st.metric(
            "Cartes retenues",
            len(corrected_labels),
        )

    validate_card_count(
        len(corrected_labels)
    )

    with st.expander(
        "Liste finale des cartes",
        expanded=False,
    ):

        dataframe = pd.DataFrame(
            {
                "Carte finale": corrected_labels
            }
        )

        st.dataframe(
            dataframe,
            use_container_width=True,
        )

    # ------------------------------------------------------------------
    # Return correction result
    # ------------------------------------------------------------------

    return {

        "corrected_labels":
            corrected_labels,

        "corrected_score":
            corrected_score,

        "corrected_score_value":
            corrected_score_value,

        "n_cards":
            len(corrected_labels),

        "rules": {

            "trump_mode":
                trump_mode,

            "trump_suit":
                trump_suit,

            "dix_de_der":
                dix_de_der,

            "include_belote_rebelote":
                include_belote_rebelote,
        },
    }