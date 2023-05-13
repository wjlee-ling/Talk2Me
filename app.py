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


openai.api_key = st.secrets["OPENAI_API_KEY"]
hide_pages(["Question1", "Question2", "Question3"])

st.title("Talk")
if "survey" not in st.session_state:
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
            st.session_state.survey = True

elif st.session_state.survey:
    st.session_state.db = init_database(user_id="admin", theme=st.session_state.leisure, n_questions=3)

    if "questions" not in st.session_state:
        st.session_state.questions = [None] +st.session_state.db.get_interview_questions(st.session_state.leisure)[:st.session_state.db.n_questions]
        st.session_state.answers = [{} for _ in range(4)]
        st.session_state.current_idx = 0
        #st.session_state.transcripts = [] * 3

    if "questions" in st.session_state:
        with st.expander(label="Q1"):
            st.session_state.current_idx = 1
            qa_template(page_idx=1)

        with st.expander(label="Q2"):
            st.session_state.current_idx = 2
            qa_template(page_idx=2)
        
        # recording_template(0)
        # st.session_state.current_idx = 2
        # recording_template(2)
        # question_template(page_idx=1)
