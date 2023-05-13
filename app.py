import typing
import random
import openai
import streamlit as st
from collections import defaultdict
from util.utils import *
from util.templates import question_template
from util.query_database import init_database
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
    st.session_state.db = init_database(user_id="admin", theme=leisure, n_questions=3)

    if "questions" not in st.session_state:
        st.session_state.questions = ["dummy"] + st.session_state.db.get_interview_questions(leisure)[:st.session_state.db.n_questions]
        st.session_state.answers = defaultdict(str)

    if "questions" in st.session_state:
        question_template(page_idx=1)
