import streamlit as st
from datetime import datetime


# Function to calculate age and category
def calculate_age_category(birth_year, current_year=datetime.now().year):
    age = current_year - birth_year
    if age <= 17:
        category = "Teenager"
    elif age < 35:
        category = "Elite"
    else:
        category = "Masters"
    return age, category


# Function to handle user login
def login():
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        st.subheader("Login / Register")

        # User Registration
        with st.form(key="register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            sex = st.radio("Sex", ["Male", "Female"])
            birth_year = st.number_input(
                "Year of Birth", min_value=1900, max_value=datetime.now().year
            )
            level = st.radio("Workout Level", ["Scaled", "RX'd"])

            submit_button = st.form_submit_button("Register")

            if submit_button:
                if not name or not email or not birth_year:
                    st.error("Please fill in all the fields.")
                else:
                    age, category = calculate_age_category(birth_year)
                    user_info = {
                        "name": name,
                        "email": email,
                        "sex": sex,
                        "birth_year": birth_year,
                        "level": level,
                        "age": age,
                        "category": category,
                    }
                    st.session_state["user"] = user_info
                    st.success(
                        f"Welcome {name}! You are categorized as {category} ({age} years old)."
                    )

        # User Login
        st.subheader("Or Login:")
        with st.form(key="login_form"):
            email_login = st.text_input("Email")
            submit_button_login = st.form_submit_button("Login")

            if submit_button_login:
                if email_login == st.session_state.get("user", {}).get("email"):
                    st.success(f"Logged in as {st.session_state['user']['name']}")
                else:
                    st.error("Email not found. Please register.")
    else:
        st.subheader(f"Hello {st.session_state['user']['name']}!")
        logout_button = st.button("Logout")
        if logout_button:
            st.session_state["user"] = None
            st.success("Logged out successfully.")


# Call the login function
login()
