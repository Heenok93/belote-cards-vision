import streamlit as st


def get_route(default="/home"):
    return st.query_params.get("nav", default)


def redirect(route: str, reload: bool = True):
    if not route.startswith("/"):
        route = "/" + route

    st.query_params["nav"] = route

    if reload:
        st.rerun()