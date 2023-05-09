import typing
import random
import openai
import streamlit as st
from collections import defaultdict
from util.utils import *
from util.database import Database
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

openai.api_key = st.secrets["OPENAI_API_KEY"]
hide_pages(["Question1", "Question2", "Question3"])

st.title("Talk")
st.header("Background Survey")
with st.form("setting"):
    st.subheader("What do you do for fun?")
    leisure = (
        st.radio(
            "Choose one of the following",
            key="leisure",
            options=["Watch movies", "Read books"],
        )
        .lower()
        .replace(" ", "_")
    )

    submitted = st.form_submit_button("Start Test")

if submitted:
    st.session_state.db = Database.init_database(user_id="admin", theme=leisure)
    st.session_state.n_questions = 3

    if "questions" not in st.session_state:
        questions = st.session_state.db.get_interview_questions(leisure)
        st.session_state.questions = ["dummy"] + random.sample(questions, st.session_state.n_questions)
        st.session_state.answers = defaultdict(str)

    switch_page("Question1")
