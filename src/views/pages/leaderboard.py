import pandas as pd
import streamlit as st

from src.services.database_service import (
    close_current_game,
    create_game,
    delete_round,
    get_current_game,
    get_rounds,
    get_score_totals,
    update_round_score,
)


def load_view():
    st.title("Scores et historique")

    game = get_current_game()
    rounds = get_rounds(game["id"])
    totals = get_score_totals(game["id"])

    st.subheader("Partie en cours")

    st.write(f"Partie #{game['id']}")
    st.write(f"Statut : **{game['status']}**")

    st.metric("Equipe 1", totals.get("Equipe 1", 0))
    st.metric("Equipe 2", totals.get("Equipe 2", 0))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Nouvelle partie", use_container_width=True):
            close_current_game(game["id"])
            create_game()
            st.rerun()

    with col2:
        if st.button("Terminer la partie", use_container_width=True):
            close_current_game(game["id"])
            st.success("Partie terminée.")
            st.rerun()

    st.divider()
    st.subheader("Manches enregistrées")

    if not rounds:
        st.info("Aucune manche enregistrée pour le moment.")
        return

    df = pd.DataFrame(rounds)

    display_df = df[
        [
            "id",
            "round_number",
            "winning_team_name",
            "winning_score",
            "photographed_team_name",
            "photographed_team_won",
            "photographed_team_score",
            "corrected_score",
            "trump_mode",
            "trump_suit",
            "created_at",
        ]
    ].rename(
        columns={
            "id": "ID",
            "round_number": "Manche",
            "winning_team_name": "Equipe gagnante",
            "winning_score": "Score enregistré",
            "photographed_team_name": "Equipe photographiée",
            "photographed_team_won": "Equipe photo gagnante",
            "photographed_team_score": "Score photo",
            "corrected_score": "Score corrigé",
            "trump_mode": "Mode",
            "trump_suit": "Atout",
            "created_at": "Date",
        }
    )

    display_df["Equipe photo gagnante"] = display_df[
        "Equipe photo gagnante"
    ].map({1: "Oui", 0: "Non"})

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("Corriger une manche")

    round_ids = [row["id"] for row in rounds]

    selected_round_id = st.selectbox(
        "Manche à modifier",
        options=round_ids,
        format_func=lambda rid: (
            f"ID {rid} - "
            f"{next(row for row in rounds if row['id'] == rid)['winning_team_name']} - "
            f"{next(row for row in rounds if row['id'] == rid)['winning_score']} points"
        ),
    )

    selected_round = next(row for row in rounds if row["id"] == selected_round_id)

    new_winning_team = st.selectbox(
        "Equipe gagnante",
        ["Equipe 1", "Equipe 2"],
        index=0 if selected_round["winning_team_name"] == "Equipe 1" else 1,
    )

    new_winning_score = st.number_input(
        "Score à enregistrer",
        min_value=0,
        max_value=182,
        value=int(selected_round["winning_score"]),
        step=1,
    )

    if new_winning_score < 82:
        st.warning(
            "Score inférieur à 82 : vérifie que c'est bien le score de l'équipe gagnante."
        )

    if st.button("Mettre à jour cette manche", use_container_width=True):
        update_round_score(
            round_id=selected_round_id,
            winning_team_name=new_winning_team,
            winning_score=int(new_winning_score),
        )
        st.success("Manche mise à jour.")
        st.rerun()

    if st.button("Supprimer cette manche", use_container_width=True):
        delete_round(selected_round_id)
        st.warning("Manche supprimée.")
        st.rerun()