"""
Detection panel.

Runs YOLO inference and displays the detection results.
"""

import streamlit as st

from src.services.inference_service import analyze_image
from src.views.components.rules_panel import DetectionSettings


# =============================================================================
# Private helpers
# =============================================================================

def _get_score_value(score):
    """Return the numeric score."""

    if hasattr(score, "total"):
        return score.total

    return score


def _validate_card_count(n_cards: int) -> None:
    """Validate the number of detected cards."""

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


def _render_detection_metrics(result: dict) -> None:
    """Display detection metrics."""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Score brut",
            _get_score_value(result["score"]),
        )

    with col2:
        st.metric(
            "Cartes valides",
            result["n_valid_cards"],
        )

    with col3:
        st.metric(
            "Cartes détectées",
            result["n_detected"],
        )

    _validate_card_count(
        result["n_valid_cards"]
    )


# =============================================================================
# Public API
# =============================================================================

def render_detection_panel(
    image_bytes: bytes,
    settings: DetectionSettings,
    preprocessing_used: bool,
    preprocessing_mode: str,
) -> dict | None:
    """
    Run YOLO inference and display the detection results.
    """

    with st.expander(
        "5. Détection IA",
        expanded=True,
    ):

        analyze_clicked = st.button(
            "Analyser l'image",
            use_container_width=True,
            type="primary",
        )

        if analyze_clicked:

            with st.spinner(
                "Analyse IA en cours..."
            ):

                result = analyze_image(
                    image_bytes=image_bytes,
                    trump_mode=settings.trump_mode,
                    trump_suit=settings.trump_suit,
                    dix_de_der=settings.dix_de_der,
                    include_belote_rebelote=settings.belote_rebelote,
                    confidence=settings.confidence,
                    image_size=settings.image_size,
                    iou=settings.iou,
                    deduplicate=settings.deduplicate,
                )

            st.session_state.analysis_result = result
            st.session_state.analysis_settings = settings

            st.session_state.analysis_preprocessing = {
                "used": preprocessing_used,
                "mode": preprocessing_mode,
            }

        result = st.session_state.get("analysis_result")

        if result is None:
            return None
        
        _render_detection_metrics(result)

        preprocessing_info = st.session_state.get(
            "analysis_preprocessing",
            {},
        )

        if preprocessing_info.get("used"):

            st.caption(
                "Prétraitement utilisé : "
                f"{preprocessing_info.get('mode')}"
            )

        else:

            st.caption(
                "Prétraitement utilisé : aucun"
            )

        if "annotated_image" in result:

            st.image(
                result["annotated_image"],
                caption="Cartes détectées par l'IA",
                use_container_width=True,
            )

        return result