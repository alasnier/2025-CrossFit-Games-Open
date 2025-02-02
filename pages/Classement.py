import streamlit as st
from pages.Authentification import engine, User, Score
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()

Session = sessionmaker(bind=engine)
session = Session()

st.title("Classement des Athlètes")

wod_selected = st.selectbox("Choisissez le WOD", ["24.1", "24.2", "24.3"])
classement = (
    session.query(User.name, User.level, User.sex, Score.score)
    .join(Score, User.id == Score.user_id)
    .filter(Score.wod == wod_selected)
    .order_by(Score.score)
    .all()
)

if classement:
    st.table(classement)
else:
    st.write("Aucun score enregistré pour ce WOD.")
