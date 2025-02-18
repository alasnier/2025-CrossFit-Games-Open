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

wod_descriptions = {
    "24.1": """
**24.1** For time (Time cap: 15 minutes)  
- 21 dumbbell snatches, arm 1  
- 21 lateral burpees over dumbbell  
- 21 dumbbell snatches, arm 2  
- 21 lateral burpees over dumbbell  
- 15 dumbbell snatches, arm 1  
- 15 lateral burpees over dumbbell  
- 15 dumbbell snatches, arm 2  
- 15 lateral burpees over dumbbell  
- 9 dumbbell snatches, arm 1  
- 9 lateral burpees over dumbbell  
- 9 dumbbell snatches, arm 2  
- 9 lateral burpees over dumbbell  
♀️ 35-lb (15-kg) dumbbell / ♂️ 50-lb (22.5-kg) dumbbell
""",
    "24.2": """
**24.2** As many rounds and reps as possible in 20 minutes:  
- 300-meter row  
- 10 deadlifts  
- 50 double-unders  
♀️ 125 lb (56 kg) / ♂️ 185 lb (83 kg)
""",
    "24.3": """
**24.3** For time (Time cap: 15 minutes)  
5 rounds of:  
- 10 thrusters (weight 1)  
- 10 chest-to-bar pull-ups  
Rest 1 minute, then:  
5 rounds of:  
- 7 thrusters (weight 2)  
- 7 bar muscle-ups  
♀️ 65, 95 lb (29, 43 kg) / ♂️ 95, 135 lb (43, 61 kg)
""",
}

score_instructions = {
    "24.1": """
🏋️ **Comment entrer votre score ?**  
- Si vous terminez avant la limite de temps (15 minutes), entrez votre temps sous le format **MM:SS**.  
- Si vous n’avez pas terminé avant le time cap :  
  - **Entrez "15:XX"**, où **XX = 1 seconde par répétition manquante**.  
  - Exemple : il vous restait 5 répétitions à faire → votre score est **15:05**.
""",
    "24.2": """
🔥 **Comment entrer votre score ?**  
- Ce WOD est un **AMRAP de 20 minutes**.  
- Entrez **le nombre total de répétitions effectuées** pendant les 20 minutes.
""",
    "24.3": """
🏋️‍♂️ **Comment entrer votre score ?**  
- Si vous terminez avant la limite de temps (15 minutes), entrez votre temps sous le format **MM:SS**.  
- Si vous n’avez pas terminé avant le time cap :  
  - **Entrez "15:XX"**, où **XX = 1 seconde par répétition manquante**.  
  - Exemple : il vous restait **7 bar muscle-ups** à faire → votre score est **15:07**.
""",
}


# Si l'utilisateur est trouvé, afficher les options de saisie
if user:
    wod = st.selectbox("Sélectionner le WOD", ["24.1", "24.2", "24.3"])
    st.markdown(f"### WOD {wod}")
    st.markdown(wod_descriptions[wod])
    st.markdown("---")
    st.markdown(score_instructions[wod])
    st.markdown("---")

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
