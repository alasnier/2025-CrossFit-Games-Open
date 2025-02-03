import streamlit as st
from pages.Authentification import engine, User, Score
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

st.title("Classement des Athlètes")

wod_selected = st.selectbox(
    "Choisissez le WOD", ["24.1", "24.2", "24.3", "Classement Général"]
)


# Fonction pour calculer les classements et récupérer les scores
def calculer_classement(wod):
    scores = (
        session.query(User.name, User.level, User.sex, Score.score)
        .join(Score, User.id == Score.user_id)
        .filter(Score.wod == wod)
        .all()
    )

    if not scores:
        return [], {}

    score_data = []
    raw_scores = {}
    for name, level, sex, score in scores:
        raw_scores.setdefault(name, {})[wod] = score
        if ":" in score:  # Score au format temps (MM:SS)
            time_parts = list(map(int, score.split(":")))
            total_seconds = time_parts[0] * 60 + time_parts[1]
            score_data.append((name, level, sex, total_seconds, "time"))
        else:  # Score basé sur les répétitions
            score_data.append((name, level, sex, int(score), "reps"))

    finished = sorted([s for s in score_data if s[4] == "time"], key=lambda x: x[3])
    not_finished = sorted(
        [s for s in score_data if s[4] == "reps"], key=lambda x: x[3], reverse=True
    )
    ranked_athletes = finished + not_finished

    total_athletes = len(ranked_athletes)
    classement = {}
    for i, (name, level, sex, score, score_type) in enumerate(ranked_athletes):
        points = total_athletes - i
        classement[name] = points

    return classement, raw_scores


if wod_selected == "Classement Général":
    general_classement = {}
    scores_details = {}
    for wod in ["24.1", "24.2", "24.3"]:
        wod_classement, wod_scores = calculer_classement(wod)
        for name, points in wod_classement.items():
            general_classement[name] = general_classement.get(name, 0) + points
            scores_details.setdefault(name, {}).update(wod_scores.get(name, {}))

    sorted_general_classement = sorted(
        general_classement.items(), key=lambda x: x[1], reverse=True
    )

    st.table(
        {
            "Nom": [c[0] for c in sorted_general_classement],
            "24.1": [
                scores_details[c[0]].get("24.1", "-") for c in sorted_general_classement
            ],
            "24.2": [
                scores_details[c[0]].get("24.2", "-") for c in sorted_general_classement
            ],
            "24.3": [
                scores_details[c[0]].get("24.3", "-") for c in sorted_general_classement
            ],
            "Points Totaux": [c[1] for c in sorted_general_classement],
        }
    )
else:
    classement, scores_details = calculer_classement(wod_selected)
    sorted_classement = sorted(classement.items(), key=lambda x: x[1], reverse=True)

    st.table(
        {
            "Nom": [c[0] for c in sorted_classement],
            "Score": [scores_details[c[0]][wod_selected] for c in sorted_classement],
            "Points": [c[1] for c in sorted_classement],
        }
    )
