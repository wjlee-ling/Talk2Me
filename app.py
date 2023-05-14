import typing
import random
import openai
import streamlit as st
from collections import defaultdict
from util.utils import *
from util.templates import qa_template
from util.query_database import init_database
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages
from util.chat import get_feedback

def update_idx(idx):
    st.session_state.current_idx = idx

openai.api_key = st.secrets["OPENAI_API_KEY"]
hide_pages(["Question1", "Question2", "Question3"])

st.title("Talk")
if "db" not in st.session_state:
    with st.form("setting"):
        st.header("Background Survey")
        st.subheader("What do you do for fun?")
        st.session_state.leisure = (
            st.radio(
                "Choose one of the following",
                options=["Watch movies", "Read books"],
            )
            .lower()
            .replace(" ", "_")
        )

        submitted = st.form_submit_button("Start Test")
        if submitted:
            st.session_state.db = init_database(user_id="admin", theme=st.session_state.leisure, n_questions=3)
            st.session_state.questions = [None] +st.session_state.db.get_interview_questions(st.session_state.leisure)[:st.session_state.db.n_questions]
            st.session_state.answers = [{} for _ in range(4)]
            st.session_state.current_idx = 1
            st.experimental_rerun()
else:
    doc = qa_template(page_idx=st.session_state.current_idx)
