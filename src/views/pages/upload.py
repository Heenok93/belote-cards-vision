"""
Upload page.
"""

import streamlit as st

from src.core.navigation import redirect, get_route

def load_view() -> None:
    """Render the upload page."""

    st.title("📤 Upload")

    st.write(
        "Charge une photographie des cartes afin de lancer l'analyse."
    )

    uploaded_file = st.file_uploader(
        "Choisir une image",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:

        st.info(
            "Sélectionne une image pour continuer."
        )

        return

    image_bytes = uploaded_file.read()

    st.session_state.uploaded_image = image_bytes

    st.image(
        image_bytes,
        caption=uploaded_file.name,
        use_container_width=True,
    )

    if st.button(
        "Analyser cette image",
        type="primary",
        use_container_width=True,
    ):

        redirect("analysis")