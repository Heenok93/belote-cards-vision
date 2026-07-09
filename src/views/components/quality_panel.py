"""
Quality analysis panel.

Displays the image quality assessment before inference.
"""

import streamlit as st

from src.services.image_quality_service import (
    ImageQualityReport,
    diagnose_image,
)


# =============================================================================
# Private helpers
# =============================================================================

def _render_quality_metrics(report: ImageQualityReport) -> None:
    """Display the main quality metrics."""

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Qualité image",
            f"{report.quality_score}/10",
        )

    with col2:
        st.metric(
            "Risque",
            report.risk_level,
        )


def _render_quality_messages(report: ImageQualityReport) -> None:
    """Display quality status."""

    if report.risk_level == "low":
        st.success(
            "Image globalement correcte pour l'inférence."
        )

    elif report.risk_level == "medium":
        st.warning(
            "Qualité moyenne : certaines conditions peuvent gêner la détection."
        )

    else:
        st.error(
            "Qualité faible : la détection peut être instable."
        )


def _render_quality_details(report: ImageQualityReport) -> None:
    """Display the detailed diagnostic."""

    with st.expander(
        "Détails du diagnostic",
        expanded=False,
    ):

        st.write(f"**Luminosité :** {report.brightness}")

        st.write(f"**Contraste :** {report.contrast}")

        st.write(f"**Netteté :** {report.blur_score}")

        st.write(
            f"**Surexposition :** {report.overexposed_pct}%"
        )

        st.divider()

        if report.issues:

            st.write("**Problèmes détectés :**")

            for issue in report.issues:
                st.write(f"- {issue}")

        else:
            st.success(
                "Aucun problème majeur détecté."
            )


# =============================================================================
# Public API
# =============================================================================

def render_quality_panel(
    image_bytes: bytes,
) -> ImageQualityReport:
    """
    Analyse the uploaded image and display
    the quality assessment panel.
    """

    report = diagnose_image(image_bytes)

    with st.expander(
        "2. Diagnostic qualité",
        expanded=True,
    ):

        _render_quality_metrics(report)

        _render_quality_messages(report)

        _render_quality_details(report)

    return report