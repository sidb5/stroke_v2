import streamlit as st
from pages.functions import add_user_to_firestore, fetch_user_from_firestore, hash_password, check_password

hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


button_style = """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)

def login_ui():
    _, col1, _ = st.columns([0.9, 2, 1])

    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary", use_container_width=True):
            if username and password:
                user_data = fetch_user_from_firestore(username)
                if user_data:
                    if check_password(user_data["password"], password):
                        st.success("Login successful!")
                        st.session_state.user = username
                        st.session_state.user_data = user_data
                        return True

                    st.error("Incorrect password. Please try again.")
                else:
                    add_user_to_firestore(
                        username,
                        {
                            "username": username,
                            "password": hash_password(password),
                        },
                    )
                    st.success("New user created and logged in!")
                    st.session_state.user = username
                    return True
            else:
                st.error("Please enter both username and password")
        return False

if login_ui():
    st.switch_page("pages/app.py")

_, col1, _ = st.columns([0.9, 2, 1])

with col1:
    if st.button("Continue without login", type="secondary", use_container_width=True):
        st.session_state.user = "guest"
        st.switch_page("pages/app.py")
