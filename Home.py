import streamlit as st

# Config default settings of the page.
st.set_page_config(
    page_title="2025 Crossfit Games Open",
    layout="wide",
    page_icon="💪",
)

# st.sidebar.success("Home")

st.markdown(" Alex lasnier - [LinkedIn](https://www.linkedin.com/in/alex-lasnier)")


# App
st.title("Welcome to the 2025 CrossFit Games Open")


st.header("""3 WEEKS - 3 WORKOUTS
                    
Workouts are released on Thursdays at 12 p.m. (PT) / 09 p.m. (Paris Hour) and scores are due by Monday at 5 p.m. (PT) / 2 a.m. (Paris Hour).""")

st.markdown("\n")

st.subheader("No matter what level you are.")
st.subheader("""There is a version of a workout for you.

Rx or Scaled """)


left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(
        "open-crossfit-2025.png",
    )

st.header("""Next stage ⇒ Semifinals

The top athletes and teams from the Open.""")
