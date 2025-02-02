import streamlit as st
from pages.Authentification import engine, User, Score
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Connexion à la base de données
Session = sessionmaker(bind=engine)
session = Session()

# Titre de la page
st.title("Saisie des Scores des WODs")

# Récupération de l'utilisateur dans la session
user = st.session_state.get("user")  # Récupère l'objet utilisateur stocké
if not user:
    st.warning("Veuillez vous connecter pour enregistrer votre score.")
    st.stop()

user_email = user["email"]
user = session.query(User).filter_by(email=user_email).first()

# Si l'utilisateur est trouvé, afficher les options de saisie
if user:
    wod = st.selectbox("Sélectionner le WOD", ["24.1", "24.2", "24.3"])

    # Initialiser la variable pour le score
    score = None

    if wod in ["24.1", "24.3"]:
        # Pour les WOD 24.1 et 24.3, on saisit un temps
        score_input = st.text_input("Entrez votre score (format HH:MM:SS)", "")

        # Validation du format du temps
        if score_input:
            try:
                score = datetime.strptime(
                    score_input, "%H:%M:%S"
                )  # Essayer de parser le temps
            except ValueError:
                st.error(
                    "Format de temps incorrect. Veuillez entrer au format HH:MM:SS."
                )
    elif wod == "24.2":
        # Pour le WOD 24.2, on saisit le nombre de répétitions
        score = st.number_input(
            "Entrez votre nombre de répétitions", min_value=0, step=1
        )

    # Vérification avant d'enregistrer le score
    if st.button("Valider"):
        if session.query(Score).filter_by(user_id=user.id, wod=wod).first():
            st.error("Vous avez déjà enregistré un score pour ce WOD.")
        else:
            # Si le score est valide, on enregistre
            if wod in ["24.1", "24.2"] and isinstance(score, datetime):
                score_str = score.strftime(
                    "%H:%M:%S"
                )  # Sauvegarder en format chaîne HH:MM:SS
            elif wod == "24.3" and isinstance(score, int) and score > 0:
                score_str = str(score)  # Sauvegarder en tant que nombre de répétitions
            else:
                st.error("Veuillez entrer un score valide.")
                st.stop()

            # Enregistrement du score dans la base de données
            new_score = Score(user_id=user.id, wod=wod, score=score_str)
            session.add(new_score)
            session.commit()
            st.success("Score enregistré avec succès !")

else:
    st.warning("Veuillez vous connecter pour enregistrer votre score.")
