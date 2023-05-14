# streamlit_app.py
# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

import streamlit as st

def check_login():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["global_passsword"]
            and st.session_state["password"]
            == st.secrets["global_passsword"][st.session_state["username"]]
        ):
            st.session_state["username"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["username"] = False

    if "username" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("What's your name?", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    
    elif not st.session_state["username"]:
        # Password not correct, show input + error.
        st.text_input("What's your name?", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known")
        return False
    else:
        # Password correct.
        return True