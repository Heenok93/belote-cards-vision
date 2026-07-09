"""
Game analysis page.

Main workflow orchestrator.
"""

import streamlit as st

from src.views.components.quality_panel import render_quality_panel
from src.views.components.preprocessing_panel import render_preprocessing_panel
from src.views.components.rules_panel import render_rules_panel
from src.views.components.detection_panel import render_detection_panel
from src.views.components.correction_panel import render_correction_panel
from src.views.components.save_panel import render_save_panel


def load_view() -> None:
    """Render the complete game analysis workflow."""

    st.title("Analyse d'une manche")

    uploaded_image = st.session_state.get("uploaded_image")

    if uploaded_image is None:
        st.warning(
            "Aucune image chargée. Revenez à la page d'accueil pour importer une photo."
        )
        return

    image_bytes = uploaded_image

    # ------------------------------------------------------------------
    # Step 1 - Image quality
    # ------------------------------------------------------------------

    report = render_quality_panel(image_bytes)

    # ------------------------------------------------------------------
    # Step 2 - Optional preprocessing
    # ------------------------------------------------------------------

    (
        image_bytes,
        preprocessing_used,
        preprocessing_mode,
    ) = render_preprocessing_panel(
        image_bytes,
        report,
    )

    # ------------------------------------------------------------------
    # Step 3 - Belote rules & AI settings
    # ------------------------------------------------------------------

    settings = render_rules_panel()

    # ------------------------------------------------------------------
    # Step 4 - Detection
    # ------------------------------------------------------------------

    detection = render_detection_panel(
        image_bytes=image_bytes,
        settings=settings,
        preprocessing_used=preprocessing_used,
        preprocessing_mode=preprocessing_mode,
    )

    if detection is None:
        return

    # ------------------------------------------------------------------
    # Step 5 - Manual correction
    # ------------------------------------------------------------------

    correction = render_correction_panel(
        result=detection,
        trump_mode=settings.trump_mode,
        trump_suit=settings.trump_suit,
        dix_de_der=settings.dix_de_der,
        include_belote_rebelote=settings.belote_rebelote,
    )

    if correction is None:
        return

    # ------------------------------------------------------------------
    # Step 6 - Save round
    # ------------------------------------------------------------------

    render_save_panel(
        detection_result=detection,
        correction_result=correction,
    )