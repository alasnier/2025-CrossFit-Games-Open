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
        return {}, {}

    classement = {}
    raw_scores = {}
    for name, level, sex, score in scores:
        raw_scores.setdefault((name, level, sex), {})[wod] = score
        if ":" in score:  # Score au format temps (MM:SS)
            time_parts = list(map(int, score.split(":")))
            total_seconds = time_parts[0] * 60 + time_parts[1]
            classement.setdefault((level, sex), []).append((name, total_seconds))
        else:  # Score basé sur les répétitions
            classement.setdefault((level, sex), []).append((name, int(score)))

    for key in classement:
        classement[key] = sorted(
            classement[key],
            key=lambda x: x[1],
            reverse=(":" not in str(classement[key][0][1])),
        )

    return classement, raw_scores


if wod_selected == "Classement Général":
    general_classement = {}
    scores_details = {}
    for wod in ["24.1", "24.2", "24.3"]:
        wod_classement, wod_scores = calculer_classement(wod)
        for (level, sex), athletes in wod_classement.items():
            for i, (name, _) in enumerate(athletes):
                general_classement.setdefault((name, level, sex), 0)
                general_classement[(name, level, sex)] += i + 1  # Points cumulés
                scores_details.setdefault((name, level, sex), {}).update(
                    wod_scores.get((name, level, sex), {})
                )

    sorted_general_classement = sorted(general_classement.items(), key=lambda x: x[1])

    st.table(
        {
            "Nom": [c[0][0] for c in sorted_general_classement],
            "Niveau": [c[0][1] for c in sorted_general_classement],
            "Sexe": [c[0][2] for c in sorted_general_classement],
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

    for (level, sex), athletes in classement.items():
        st.subheader(f"Classement {level} - {sex}")
        sorted_classement = [
            (name, scores_details[(name, level, sex)][wod_selected])
            for name, _ in athletes
        ]
        st.table(
            {
                "Nom": [c[0] for c in sorted_classement],
                "Score": [c[1] for c in sorted_classement],
                "Points": [i + 1 for i in range(len(sorted_classement))],
            }
        )
