import streamlit as st
from ..repositories.auth import authenticate_user

def show_login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        auth_result = authenticate_user(username, password)
        if auth_result["authenticated"]:
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = auth_result["user_id"]
            st.session_state["role_id"] = auth_result["role_id"]
            st.session_state["username"] = auth_result["username"]
        else:
            st.warning("Invalid username or password")