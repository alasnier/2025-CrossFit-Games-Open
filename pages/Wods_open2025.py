import streamlit as st


# Config default settings of the page.


st.set_page_config(
    page_title="Wods open2025",
    layout="wide",
    page_icon="2025",
)

left_co, cent_co, last_co = st.columns(3)
with left_co:
    st.markdown(
        "**25.1**   As many rounds and reps as possible in 15 minutes of :",
    )
with cent_co:
    st.markdown("""
3 lateral burpees over the dumbbell \n
3 dumbbell hang clean-to-overheads \n
30-foot walking lunge (2 x 15 feet) \n
""")
    st.markdown("")
    st.markdown(
        "**After completing each round, add 3 reps to the burpees and hang clean-to-overheads.**"
    )
with last_co:
    st.markdown("""
♀️ 35-lb (15-kg) dumbbell

♂️ 50-lb (22.5-kg) dumbbell""")

st.markdown(
    "---"
)  # ----------------------------------------------------------------------------------------------------
