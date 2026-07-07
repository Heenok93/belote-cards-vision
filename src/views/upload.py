import streamlit as st
from src.router import redirect


def load_view():
    st.title("📤 Upload de partie")

    st.markdown(
        "Ajoutez une photo de cartes afin de lancer l'analyse automatique."
    )

    uploaded_file = st.file_uploader(
        "Choisissez une image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.session_state["uploaded_image_bytes"] = uploaded_file.getvalue()
        st.session_state["uploaded_image_name"] = uploaded_file.name

        st.image(uploaded_file, caption="Image chargée", use_container_width=True)

        if st.button("Lancer l'analyse"):
            redirect("analysis", reload=True)
    else:
        st.info("Chargez une image pour activer l'analyse.")