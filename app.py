import openai
import streamlit as st
from util.utils import *
from util.templates import qa_template, feedback_template, user_feedback_template
from util.query_database import init_database
from streamlit import session_state as sst


openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Talk2Ava")
if "db" not in sst:
    if "current_idx" in sst and sst.current_idx > 0:
        st.cache_resource.clear()
        
    with st.form("setting"):
        st.header("Background Survey")
        st.subheader("Who are you?")
        st.text_input(label="Let me know your English nickname.", value="", key="username")
        if len(sst.username) == 0:
            st.warning("닉네임을 입력해 주세요!")
        st.subheader("What do you do for fun?")
        sst.leisure = (
            st.radio(
                "Choose one of the following:",
                options=["Watch movies", "Read books"],
            )
            .lower()
            .replace(" ", "_")
        )

        submitted = st.form_submit_button("Start Test")
        if submitted and len(sst.username) > 0:
            sst.db = init_database(user_id=sst.username, theme=sst.leisure, n_questions=3)
            sst.questions = [None] + sst.db.get_interview_questions(sst.leisure)[: sst.db.n_questions]
            sst.answers = [{} for _ in range(4)]
            sst.current_idx = 1
            sst.user_feedback = "first_run"
            st.experimental_rerun()
else:
    if sst.current_idx > sst.db.n_questions: # To-do : n_themes * n_questions:
        if sst.user_feedback == "first_run":
            feedback_template(page_idx=sst.current_idx)
        elif sst.user_feedback == "not_yet":
            user_feedback_template(page_idx=sst.current_idx)
        elif sst.user_feedback == "sent":
            feedback_template(page_idx=sst.current_idx)
            
    else:
        qa_template(page_idx=sst.current_idx)
