"""
Image preprocessing panel.

Displays preprocessing recommendations and allows the user
to preview and apply image preprocessing before inference.
"""

import streamlit as st

from src.services.image_preprocessing_service import preprocess_image
from src.services.image_quality_service import ImageQualityReport


# =============================================================================
# Labels
# =============================================================================

PREPROCESSING_LABELS = {
    "none": "Aucun",
    "auto": "Auto léger recommandé",
    "clahe": "Contraste local CLAHE",
    "darken": "Assombrir / réduire la surexposition",
    "brighten": "Éclaircir",
    "sharpen": "Netteté légère",
}


# =============================================================================
# Private helpers
# =============================================================================

def _render_recommendation(report: ImageQualityReport) -> None:
    """Display the recommended preprocessing."""

    if report.recommended_preprocessing == "none":
        st.info(
            "Aucun prétraitement n'est recommandé pour cette image."
        )
        return

    label = PREPROCESSING_LABELS.get(
        report.recommended_preprocessing,
        report.recommended_preprocessing,
    )

    st.info(
        f"Prétraitement conseillé : {label}"
    )


# =============================================================================
# Public API
# =============================================================================

def render_preprocessing_panel(
    image_bytes: bytes,
    report: ImageQualityReport,
) -> tuple[bytes, bool, str]:
    """
    Display the preprocessing panel.

    Returns
    -------
    image_bytes
        Image that will be used for inference.

    use_preprocessing
        Whether preprocessing has been applied.

    preprocessing_mode
        Selected preprocessing mode.
    """

    image_bytes_for_inference = image_bytes

    with st.expander(
        "3. Prétraitement optionnel",
        expanded=report.risk_level != "low",
    ):

        _render_recommendation(report)

        preprocessing_keys = list(
            PREPROCESSING_LABELS.keys()
        )

        preprocessing_mode = st.selectbox(
            "Mode de prétraitement",
            options=preprocessing_keys,
            format_func=lambda mode: PREPROCESSING_LABELS[mode],
            index=preprocessing_keys.index(
                report.recommended_preprocessing
            ),
        )

        use_preprocessing = st.checkbox(
            "Utiliser l'image prétraitée pour l'inférence",
            value=False,
        )

        if (
            use_preprocessing
            and preprocessing_mode != "none"
        ):

            try:

                image_bytes_for_inference = preprocess_image(
                    image_bytes,
                    mode=preprocessing_mode,
                )

                st.image(
                    image_bytes_for_inference,
                    caption=(
                        "Image prétraitée — "
                        f"{PREPROCESSING_LABELS[preprocessing_mode]}"
                    ),
                    use_container_width=True,
                )

            except Exception as exc:

                st.error(
                    f"Prétraitement impossible : {exc}"
                )

                image_bytes_for_inference = image_bytes

    return (
        image_bytes_for_inference,
        use_preprocessing,
        preprocessing_mode,
    )