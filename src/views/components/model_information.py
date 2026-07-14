"""
Model information component.
"""

from __future__ import annotations

import streamlit as st

from config.settings import (
    DEFAULT_CONFIDENCE,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_IOU,
    DEFAULT_MODEL_PATH,
    MODEL_INFORMATION_TITLE,
)


# =============================================================================
# Public API
# =============================================================================

def render_model_information() -> None:
    """
    Display model information.
    """

    st.subheader(MODEL_INFORMATION_TITLE)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Modèle",
            DEFAULT_MODEL_PATH.name,
        )

        st.metric(
            "Confiance",
            DEFAULT_CONFIDENCE,
        )

    with col2:

        st.metric(
            "IOU",
            DEFAULT_IOU,
        )

        st.metric(
            "Image",
            DEFAULT_IMAGE_SIZE,
        )