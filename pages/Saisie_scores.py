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
    st.warning(
        "Veuillez vous connecter pour enregistrer votre score => onglet Authentification (Barre Laterale Gauche)"
    )
    st.stop()

user_email = user["email"]
user = session.query(User).filter_by(email=user_email).first()

# Si l'utilisateur est trouvé, afficher les options de saisie
if user:
    wod = st.selectbox("Sélectionner le WOD", ["24.1", "24.2", "24.3"])

    # Vérifier si l'utilisateur a déjà enregistré un score
    existing_score = session.query(Score).filter_by(user_id=user.id, wod=wod).first()

    if existing_score:
        st.warning(f"Score actuel pour {wod} : {existing_score.score}")
        modify = st.checkbox("Modifier votre score ?")
    else:
        modify = True

    if modify:
        new_score = None
        if wod in ["24.1", "24.3"]:
            score_input = st.text_input(
                "Entrez votre score (format MM:SS)",
                existing_score.score if existing_score else "",
            )
            try:
                new_score = datetime.strptime(score_input, "%M:%S").strftime("%M:%S")
            except ValueError:
                st.error("Format de temps incorrect. Utilisez MM:SS.")
        elif wod == "24.2":
            new_score = st.number_input(
                "Entrez votre nombre de répétitions",
                min_value=0,
                step=1,
                value=int(existing_score.score) if existing_score else 0,
            )

        if st.button("Enregistrer" if not existing_score else "Mettre à jour"):
            if new_score:
                if existing_score:
                    existing_score.score = str(new_score)
                else:
                    new_score_entry = Score(
                        user_id=user.id, wod=wod, score=str(new_score)
                    )
                    session.add(new_score_entry)
                session.commit()
                st.success("Score enregistré avec succès !")
else:
    st.warning(
        "Veuillez vous connecter pour enregistrer votre score => onglet Authentification (Barre Laterale Gauche)"
    )
