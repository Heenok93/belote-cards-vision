import pandas as pd
import streamlit as st

from src.core.navigation import redirect
from src.core.session import reset_analysis

from src.services.database_service import (
    close_current_game,
    delete_round,
    get_current_game,
    get_rounds,
    get_score_totals,
    update_round_score,
)


def load_view():

    st.title("🏆 Scores et historique")

    game = get_current_game()
    rounds = get_rounds(game["id"])
    totals = get_score_totals(game["id"])

    team1 = totals.get("Equipe 1", 0)
    team2 = totals.get("Equipe 2", 0)

    st.subheader("Partie en cours")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Partie #{game['id']}**")
        st.write(f"Statut : **{game['status']}**")
        st.write(f"**{len(rounds)} manche(s) enregistrée(s)**")

    with col2:

        if team1 > team2:
            leader = "Equipe 1"
            diff = team1 - team2

        elif team2 > team1:
            leader = "Equipe 2"
            diff = team2 - team1

        else:
            leader = "Égalité"
            diff = 0

        if leader == "Égalité":
            st.info("🤝 Les deux équipes sont à égalité.")
        else:
            st.success(
                f"🏆 Leader actuel : **{leader}** (+{diff} pts)"
            )

    st.divider()

    score_col1, score_col2 = st.columns(2)

    with score_col1:
        st.metric(
            "Equipe 1",
            team1,
        )

    with score_col2:
        st.metric(
            "Equipe 2",
            team2,
        )

    st.divider()

    action_col1, action_col2 = st.columns(2)

    with action_col1:

        if st.button(
            "📸 Nouvelle manche",
            use_container_width=True,
        ):

            reset_analysis()
            redirect("upload")

    with action_col2:

        if st.button(
            "🏁 Terminer la partie",
            type="primary",
            use_container_width=True,
        ):

            close_current_game(game["id"])

            reset_analysis()

            st.success("Partie terminée.")

            redirect("home")

    st.divider()

    st.subheader("📋 Historique des manches")

    if not rounds:

        st.info(
            "Aucune manche enregistrée pour le moment."
        )

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
            "winning_score": "Score",
            "photographed_team_name": "Equipe photographiée",
            "photographed_team_won": "Victoire photo",
            "photographed_team_score": "Score photo",
            "corrected_score": "Score corrigé",
            "trump_mode": "Mode",
            "trump_suit": "Atout",
            "created_at": "Date",
        }
    )

    display_df["Victoire photo"] = display_df[
        "Victoire photo"
    ].map(
        {
            1: "Oui",
            0: "Non",
        }
    )

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    st.subheader("✏️ Corriger une manche")

    round_ids = [
        row["id"]
        for row in rounds
    ]

    selected_round_id = st.selectbox(
        "Sélectionner une manche",
        options=round_ids,
        format_func=lambda rid: (
            f"Manche {next(r for r in rounds if r['id']==rid)['round_number']} "
            f"• "
            f"{next(r for r in rounds if r['id']==rid)['winning_team_name']} "
            f"({next(r for r in rounds if r['id']==rid)['winning_score']} pts)"
        ),
    )

    selected_round = next(
        row
        for row in rounds
        if row["id"] == selected_round_id
    )

    new_team = st.selectbox(
        "Equipe gagnante",
        [
            "Equipe 1",
            "Equipe 2",
        ],
        index=0
        if selected_round["winning_team_name"] == "Equipe 1"
        else 1,
    )

    new_score = st.number_input(
        "Score de l'équipe gagnante",
        min_value=0,
        max_value=182,
        value=int(selected_round["winning_score"]),
        step=1,
    )

    if new_score < 82:

        st.warning(
            "Le score est inférieur à 82 points."
        )

    col_update, col_delete = st.columns(2)

    with col_update:

        if st.button(
            "💾 Mettre à jour",
            use_container_width=True,
        ):

            update_round_score(
                round_id=selected_round_id,
                winning_team_name=new_team,
                winning_score=int(new_score),
            )

            st.success("Manche mise à jour.")

            st.rerun()

    with col_delete:

        if st.button(
            "🗑️ Supprimer",
            use_container_width=True,
        ):

            delete_round(selected_round_id)

            st.warning("Manche supprimée.")

            st.rerun()