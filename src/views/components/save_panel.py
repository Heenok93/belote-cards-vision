"""
Save panel.

Validates and persists the corrected Belote round.
"""

import streamlit as st

from src.services.database_service import (
    get_current_game,
    get_score_totals,
    save_round_score,
)


# =============================================================================
# Public API
# =============================================================================

def render_save_panel(
    detection_result: dict,
    correction_result: dict,
) -> None:
    """
    Display the save workflow.
    """

    st.divider()

    st.subheader(
        "Enregistrer la manche"
    )

    game = get_current_game()

    photographed_team = st.radio(
        "Equipe photographiée",
        [
            "Equipe 1",
            "Equipe 2",
        ],
        horizontal=True,
    )

    photographed_team_won = (

        st.radio(
            "Cette équipe a gagné la manche ?",
            [
                "Oui",
                "Non",
            ],
            horizontal=True,
        )

        == "Oui"
    )

    raw_score = detection_result["score"]

    if hasattr(raw_score, "total"):
        raw_score = raw_score.total

    photographed_score = correction_result[
        "corrected_score_value"
    ]

    opponent_team = (
        "Equipe 2"
        if photographed_team == "Equipe 1"
        else "Equipe 1"
    )

    if photographed_team_won:

        winning_team = photographed_team
        winning_score = photographed_score

    else:

        winning_team = opponent_team
        winning_score = 162 - photographed_score

    st.write(
        "Score qui sera enregistré :"
    )

    st.metric(
        winning_team,
        winning_score,
    )

    # -------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------

    score_is_valid = True

    if photographed_score < 0:

        st.error(
            "Score impossible."
        )

        score_is_valid = False

    if photographed_score > 162:

        st.warning(
            "Score supérieur à 162. "
            "Vérifie les corrections."
        )

    if winning_score < 0:

        st.error(
            "Le score gagnant est négatif."
        )

        score_is_valid = False

    if winning_score > 182:

        st.error(
            "Le score dépasse 182."
        )

        score_is_valid = False

    if winning_score < 82:

        st.warning(
            "Le score gagnant est inférieur à 82."
        )

    # -------------------------------------------------------------
    # Save
    # -------------------------------------------------------------

    if st.button(
        "Enregistrer cette manche",
        type="primary",
        use_container_width=True,
        disabled=not score_is_valid,
    ):

        rules = correction_result["rules"]

        save_round_score(

            game_id=game["id"],

            winning_team_name=winning_team,

            winning_score=winning_score,

            photographed_team_name=photographed_team,

            photographed_team_won=photographed_team_won,

            photographed_team_score=photographed_score,

            raw_score=raw_score,

            corrected_score=photographed_score,

            cards=correction_result[
                "corrected_labels"
            ],

            trump_mode=rules[
                "trump_mode"
            ].name,

            trump_suit=(
                rules["trump_suit"].name
                if rules["trump_suit"]
                else None
            ),

            dix_de_der=rules[
                "dix_de_der"
            ],

            belote_rebelote=rules[
                "include_belote_rebelote"
            ],
        )

        st.success(
            f"Manche enregistrée : "
            f"{winning_team} marque "
            f"{winning_score} points."
        )

    # -------------------------------------------------------------
    # Running score
    # -------------------------------------------------------------

    totals = get_score_totals(
        game["id"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Equipe 1",
            totals.get(
                "Equipe 1",
                0,
            ),
        )

    with col2:

        st.metric(
            "Equipe 2",
            totals.get(
                "Equipe 2",
                0,
            ),
        )