import pandas as pd
import streamlit as st

from src.services.inference_service import analyze_image
from src.services.image_quality_service import diagnose_image
from src.services.image_preprocessing_service import preprocess_image
from src.services.database_service import (
    get_current_game,
    get_score_totals,
    save_round_score,
)

from src.game.belote.cards import Suit, parse_card
from src.game.belote.scoring import TrumpMode, compute_score


ALL_CARD_LABELS = [
    "7_TREFLE", "7_CARREAU", "7_COEUR", "7_PIQUE",
    "8_TREFLE", "8_CARREAU", "8_COEUR", "8_PIQUE",
    "9_TREFLE", "9_CARREAU", "9_COEUR", "9_PIQUE",
    "10_TREFLE", "10_CARREAU", "10_COEUR", "10_PIQUE",
    "VALET_TREFLE", "VALET_CARREAU", "VALET_COEUR", "VALET_PIQUE",
    "DAME_TREFLE", "DAME_CARREAU", "DAME_COEUR", "DAME_PIQUE",
    "ROI_TREFLE", "ROI_CARREAU", "ROI_COEUR", "ROI_PIQUE",
    "AS_TREFLE", "AS_CARREAU", "AS_COEUR", "AS_PIQUE",
]

PREPROCESSING_LABELS = {
    "none": "Aucun",
    "auto": "Auto léger recommandé",
    "clahe": "Contraste local CLAHE",
    "darken": "Assombrir / réduire surexposition",
    "brighten": "Éclaircir",
    "sharpen": "Netteté légère",
}


def get_score_value(score):
    if hasattr(score, "total"):
        return score.total
    return score


def deduplicate_labels(labels: list[str]) -> list[str]:
    return list(dict.fromkeys(labels))


def validate_card_count(n_cards: int):
    if n_cards == 0:
        st.warning("Aucune carte retenue pour le score final.")
    elif n_cards > 32:
        st.error("Plus de 32 cartes retenues : impossible pour une partie de Belote.")
    elif n_cards % 4 != 0:
        st.warning(
            "Nombre de cartes suspect : le total devrait être un multiple de 4 "
            "(4, 8, 12, ..., 32)."
        )
    else:
        st.success("Nombre de cartes cohérent avec une distribution de Belote.")


def compute_corrected_score(
    labels: list[str],
    trump_mode: TrumpMode,
    trump_suit: Suit | None,
    dix_de_der: bool,
    include_belote_rebelote: bool,
):
    cards = [parse_card(label) for label in labels]

    return compute_score(
        cards=cards,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )


def render_quality_report(report):
    st.metric("Qualité image", f"{report.quality_score}/10")
    st.metric("Risque", report.risk_level)

    if report.risk_level == "low":
        st.success("Image globalement correcte pour l'inférence.")
    elif report.risk_level == "medium":
        st.warning("Qualité moyenne : certaines conditions peuvent gêner la détection.")
    else:
        st.error("Qualité faible : la détection peut être instable.")

    with st.expander("Détails du diagnostic"):
        st.write(f"**Luminosité :** {report.brightness}")
        st.write(f"**Contraste :** {report.contrast}")
        st.write(f"**Netteté :** {report.blur_score}")
        st.write(f"**Surexposition :** {report.overexposed_pct}%")

        st.divider()

        if report.issues:
            st.write("**Problèmes détectés :**")
            for issue in report.issues:
                st.write(f"- {issue}")
        else:
            st.write("Aucun problème majeur détecté.")


def render_scoring_rules():
    mode_label = st.selectbox(
        "Mode de jeu",
        ["Classique", "Tout Atout", "Sans Atout"],
    )

    if mode_label == "Classique":
        trump_mode = TrumpMode.CLASSIC
        trump_suit_label = st.selectbox(
            "Atout",
            ["COEUR", "CARREAU", "PIQUE", "TREFLE"],
        )
        trump_suit = Suit[trump_suit_label]

        include_belote_rebelote = st.checkbox(
            "Belote / Rebelote",
            value=True,
        )

    elif mode_label == "Tout Atout":
        trump_mode = TrumpMode.ALL_TRUMP
        trump_suit = None
        include_belote_rebelote = False
        st.info("Toutes les couleurs sont à l'atout.")

    else:
        trump_mode = TrumpMode.NO_TRUMP
        trump_suit = None
        include_belote_rebelote = False
        st.info("Aucune couleur n'est à l'atout.")

    dix_de_der = st.checkbox("Dix de Der", value=False)

    return trump_mode, trump_suit, dix_de_der, include_belote_rebelote


def render_rules_summary(
    trump_mode,
    trump_suit,
    dix_de_der,
    include_belote_rebelote,
):
    mode_name = {
        TrumpMode.CLASSIC: "Classique",
        TrumpMode.ALL_TRUMP: "Tout Atout",
        TrumpMode.NO_TRUMP: "Sans Atout",
    }.get(trump_mode, str(trump_mode))

    st.write("Règles utilisées :")
    st.write(f"- Mode : **{mode_name}**")

    if trump_suit is not None:
        st.write(f"- Atout : **{trump_suit.name}**")

    st.write(f"- Dix de Der : **{'Oui' if dix_de_der else 'Non'}**")
    st.write(
        "- Belote / Rebelote : "
        f"**{'Oui' if include_belote_rebelote else 'Non'}**"
    )


def render_detection_metrics(result):
    st.metric("Score brut", get_score_value(result["score"]))
    st.metric("Cartes valides", result["n_valid_cards"])
    st.metric("Cartes détectées par l'IA", result["n_detected"])

    validate_card_count(result["n_valid_cards"])


def render_mobile_correction(detections):
    corrected_labels = []

    for i, detection in enumerate(detections):
        label = detection["label"]
        confidence = round(detection["confidence"], 3)

        st.markdown(f"**Carte {i + 1} — {label}**")
        st.caption(f"Confiance IA : {confidence}")

        keep = st.checkbox(
            "Garder cette carte",
            value=True,
            key=f"keep_card_{i}",
        )

        default_label = label if label in ALL_CARD_LABELS else ALL_CARD_LABELS[0]
        default_index = ALL_CARD_LABELS.index(default_label)

        corrected_label = st.selectbox(
            "Carte corrigée",
            options=ALL_CARD_LABELS,
            index=default_index,
            key=f"corrected_card_{i}",
        )

        if keep:
            corrected_labels.append(corrected_label)

        st.divider()

    return corrected_labels


def render_table_correction(detections):
    correction_rows = [
        {
            "Garder": True,
            "Carte détectée": d["label"],
            "Carte corrigée": d["label"] if d["valid"] else ALL_CARD_LABELS[0],
            "Confiance": round(d["confidence"], 3),
        }
        for d in detections
    ]

    correction_df = pd.DataFrame(correction_rows)

    edited_df = st.data_editor(
        correction_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Garder": st.column_config.CheckboxColumn(
                "Garder",
                help="Décoche pour supprimer une fausse détection.",
            ),
            "Carte détectée": st.column_config.TextColumn(
                "Carte détectée",
                disabled=True,
            ),
            "Carte corrigée": st.column_config.SelectboxColumn(
                "Carte corrigée",
                options=ALL_CARD_LABELS,
            ),
            "Confiance": st.column_config.NumberColumn(
                "Confiance",
                disabled=True,
                format="%.3f",
            ),
        },
        key="card_correction_editor",
    )

    return edited_df.loc[
        edited_df["Garder"],
        "Carte corrigée",
    ].tolist()


def render_save_score_section(
    result,
    corrected_score,
    corrected_labels,
    trump_mode,
    trump_suit,
    dix_de_der,
    include_belote_rebelote,
):
    st.divider()
    st.subheader("Enregistrer la manche")

    game = get_current_game()

    photographed_team = st.radio(
        "Equipe photographiée",
        ["Equipe 1", "Equipe 2"],
        horizontal=True,
    )

    photographed_team_won = st.radio(
        "Cette équipe a gagné la manche ?",
        ["Oui", "Non"],
        horizontal=True,
    ) == "Oui"

    raw_score = get_score_value(result["score"])
    photographed_score = int(get_score_value(corrected_score))

    opponent_team = "Equipe 2" if photographed_team == "Equipe 1" else "Equipe 1"

    if photographed_team_won:
        winning_team = photographed_team
        winning_score = photographed_score
    else:
        winning_team = opponent_team
        winning_score = 162 - photographed_score

    st.write("Score qui sera enregistré :")
    st.metric(winning_team, winning_score)

    score_is_valid = True

    if photographed_score < 0:
        st.error("Score impossible : le score photographié ne peut pas être négatif.")
        score_is_valid = False

    if photographed_score > 162:
        st.warning(
            "Score supérieur à 162. Vérifie si Belote/Rebelote est incluse "
            "ou si une correction manuelle est nécessaire."
        )

    if winning_score < 0:
        st.error(
            "Score gagnant impossible : le calcul donne un score négatif. "
            "Vérifie l'équipe gagnante ou le score corrigé."
        )
        score_is_valid = False

    if winning_score > 182:
        st.error(
            "Score gagnant impossible : le score dépasse 182 points. "
            "Vérifie les cartes, Dix de Der et Belote/Rebelote."
        )
        score_is_valid = False

    if winning_score < 82:
        st.warning(
            "Le score enregistré est inférieur à 82. "
            "En Belote, l'équipe gagnante devrait généralement avoir au moins 82 points."
        )

    if st.button(
        "Enregistrer cette manche",
        use_container_width=True,
        type="primary",
        disabled=not score_is_valid,
    ):
        save_round_score(
            game_id=game["id"],
            winning_team_name=winning_team,
            winning_score=winning_score,
            photographed_team_name=photographed_team,
            photographed_team_won=photographed_team_won,
            photographed_team_score=photographed_score,
            raw_score=raw_score,
            corrected_score=photographed_score,
            cards=corrected_labels,
            trump_mode=trump_mode.name,
            trump_suit=trump_suit.name if trump_suit is not None else None,
            dix_de_der=dix_de_der,
            belote_rebelote=include_belote_rebelote,
        )

        st.success(
            f"Manche enregistrée : {winning_team} marque {winning_score} points."
        )

    totals = get_score_totals(game["id"])

    st.write("Score cumulé")
    st.metric("Equipe 1", totals.get("Equipe 1", 0))
    st.metric("Equipe 2", totals.get("Equipe 2", 0))

def render_correction_interface(
    result,
    trump_mode,
    trump_suit,
    dix_de_der,
    include_belote_rebelote,
):
    detections = result["detections"]

    if not detections:
        st.warning(
            "Aucune carte détectée. Essaie de baisser le seuil de confiance "
            "ou d'utiliser une photo plus nette."
        )
        return

    correction_mode = st.radio(
        "Mode de correction",
        ["Correction simple", "Tableau avancé"],
        horizontal=False,
    )

    if correction_mode == "Correction simple":
        corrected_labels = render_mobile_correction(detections)
    else:
        corrected_labels = render_table_correction(detections)

    with st.expander("Ajouter des cartes manquantes", expanded=False):
        added_cards = st.multiselect(
            "Cartes à ajouter",
            options=ALL_CARD_LABELS,
            default=[],
        )
        corrected_labels.extend(added_cards)

    corrected_labels = deduplicate_labels(corrected_labels)

    corrected_score = compute_corrected_score(
        labels=corrected_labels,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )

    st.session_state["corrected_labels"] = corrected_labels
    st.session_state["corrected_score_value"] = get_score_value(corrected_score)

    st.subheader("Score final corrigé")
    st.metric("Score corrigé", get_score_value(corrected_score))
    st.metric("Cartes retenues", len(corrected_labels))

    validate_card_count(len(corrected_labels))

    with st.expander("Liste finale des cartes"):
        st.dataframe(
            pd.DataFrame({"Carte finale": corrected_labels}),
            use_container_width=True,
        )

    render_save_score_section(
        result=result,
        corrected_score=corrected_score,
        corrected_labels=corrected_labels,
        trump_mode=trump_mode,
        trump_suit=trump_suit,
        dix_de_der=dix_de_der,
        include_belote_rebelote=include_belote_rebelote,
    )


def reset_analysis():
    for key in [
        "analysis_result",
        "analysis_rules",
        "analysis_preprocessing",
        "card_correction_editor",
        "corrected_labels",
        "corrected_score_value",
    ]:
        st.session_state.pop(key, None)

    st.rerun()


def load_view():
    st.title("Analyse automatique des cartes")

    st.info(
        "Workflow : qualité image → prétraitement → règles → détection IA "
        "→ correction manuelle → score final."
    )

    if "uploaded_image_bytes" not in st.session_state:
        st.warning("Aucune image chargée. Va d'abord dans la page Upload.")
        return

    image_bytes_original = st.session_state["uploaded_image_bytes"]
    image_bytes_for_inference = image_bytes_original

    if st.button("Réinitialiser l'analyse", use_container_width=True):
        reset_analysis()

    with st.expander("1. Image originale", expanded=True):
        st.image(
            image_bytes_original,
            caption=st.session_state.get("uploaded_image_name", "Image chargée"),
            use_container_width=True,
        )

    report = diagnose_image(image_bytes_original)

    with st.expander("2. Diagnostic qualité", expanded=True):
        render_quality_report(report)

    with st.expander(
        "3. Prétraitement optionnel",
        expanded=report.risk_level != "low",
    ):
        recommended_mode = report.recommended_preprocessing

        if recommended_mode == "none":
            st.info("Aucun prétraitement n'est recommandé pour cette image.")
        else:
            st.info(
                "Prétraitement conseillé : "
                f"{PREPROCESSING_LABELS.get(recommended_mode, recommended_mode)}"
            )

        preprocessing_keys = list(PREPROCESSING_LABELS.keys())

        preprocessing_mode = st.selectbox(
            "Mode de prétraitement",
            options=preprocessing_keys,
            format_func=lambda x: PREPROCESSING_LABELS[x],
            index=preprocessing_keys.index(recommended_mode),
        )

        use_preprocessing = st.checkbox(
            "Utiliser l'image prétraitée pour l'inférence",
            value=False,
        )

        if use_preprocessing and preprocessing_mode != "none":
            try:
                image_bytes_for_inference = preprocess_image(
                    image_bytes_original,
                    mode=preprocessing_mode,
                )

                st.image(
                    image_bytes_for_inference,
                    caption=(
                        "Image prétraitée - "
                        f"{PREPROCESSING_LABELS[preprocessing_mode]}"
                    ),
                    use_container_width=True,
                )

            except Exception as exc:
                st.error(f"Prétraitement impossible : {exc}")
                image_bytes_for_inference = image_bytes_original

    with st.expander("4. Règles de scoring", expanded=True):
        trump_mode, trump_suit, dix_de_der, include_belote_rebelote = (
            render_scoring_rules()
        )

        render_rules_summary(
            trump_mode=trump_mode,
            trump_suit=trump_suit,
            dix_de_der=dix_de_der,
            include_belote_rebelote=include_belote_rebelote,
        )

        with st.expander("Paramètres avancés IA"):
            conf = st.slider(
                "Seuil de confiance",
                min_value=0.05,
                max_value=0.90,
                value=0.10,
                step=0.05,
                help=(
                    "Plus le seuil est bas, plus l'IA garde de détections. "
                    "Utile si certaines cartes sont manquées."
                ),
            )

            imgsz = st.selectbox(
                "Taille image YOLO",
                options=[768, 1024, 1280],
                index=1,
                help="Taille utilisée par le modèle pour analyser l'image.",
            )

            iou = st.slider(
                "NMS IoU",
                min_value=0.30,
                max_value=0.90,
                value=0.65,
                step=0.05,
                help="Paramètre technique contrôlant la suppression des doublons.",
            )

    with st.expander("5. Détection IA", expanded=True):
        analyze_clicked = st.button(
            "Analyser l'image",
            use_container_width=True,
            type="primary",
        )

        if analyze_clicked:
            with st.spinner("Analyse IA en cours..."):
                result = analyze_image(
                    image_bytes=image_bytes_for_inference,
                    trump_mode=trump_mode,
                    trump_suit=trump_suit,
                    dix_de_der=dix_de_der,
                    include_belote_rebelote=include_belote_rebelote,
                    conf=conf,
                    imgsz=imgsz,
                    iou=iou,
                )

            st.session_state["analysis_result"] = result
            st.session_state["analysis_rules"] = {
                "trump_mode": trump_mode,
                "trump_suit": trump_suit,
                "dix_de_der": dix_de_der,
                "include_belote_rebelote": include_belote_rebelote,
            }
            st.session_state["analysis_preprocessing"] = {
                "used": use_preprocessing,
                "mode": preprocessing_mode,
            }

        if "analysis_result" in st.session_state:
            result = st.session_state["analysis_result"]

            render_detection_metrics(result)

            preprocessing_info = st.session_state.get("analysis_preprocessing", {})
            if preprocessing_info.get("used"):
                mode = preprocessing_info.get("mode", "none")
                st.caption(
                    "Prétraitement utilisé : "
                    f"{PREPROCESSING_LABELS.get(mode, mode)}"
                )
            else:
                st.caption("Prétraitement utilisé : aucun")

            if "annotated_image" in result:
                st.image(
                    result["annotated_image"],
                    caption="Cartes détectées par l'IA",
                    use_container_width=True,
                )

    if "analysis_result" not in st.session_state:
        return

    with st.expander("6. Correction et score final", expanded=True):
        result = st.session_state["analysis_result"]
        rules = st.session_state.get("analysis_rules", {})

        render_correction_interface(
            result=result,
            trump_mode=rules.get("trump_mode", trump_mode),
            trump_suit=rules.get("trump_suit", trump_suit),
            dix_de_der=rules.get("dix_de_der", dix_de_der),
            include_belote_rebelote=rules.get(
                "include_belote_rebelote",
                include_belote_rebelote,
            ),
        )