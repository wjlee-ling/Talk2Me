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

    if "current_idx" not in st.session_state:
        st.session_state.questions = [None] +st.session_state.db.get_interview_questions(st.session_state.leisure)[:st.session_state.db.n_questions]
        st.session_state.answers = [{} for _ in range(4)]
        st.session_state.current_idx = 0
        st.experimental_rerun()
        #st.session_state.transcripts = [] * 3

    else:
        if st.session_state.current_idx > 0:
            doc = qa_template(st.session_state.current_idx)

        if st.button(label="Q1  ▽", use_container_width=True, key="bttn1", on_click=update_idx, args=[1]):
            st.empty()
            # st.session_state.current_idx = 1  
            # doc = qa_template(st.session_state.current_idx)
        
        if st.button(label="Q2  ▽", use_container_width=True, key="bttn2"):
            st.session_state.current_idx = 2
            # doc = qa_template(st.session_state.current_idx)

            # if st.session_state.answers[1] != {}:
            #     st.write(st.session_state.answers[1]["transcript"])
                # if "feedback" in st.session_state.answers[1]:
                #     st.write(st.session_state.answers[1]["feedback"])
                # else: 
                    # if st.button("Get Feedback", key=f"feedback_button_{1}"):
                    #     feedback = get_feedback(doc)
                    #     st.session_state.db.update_feedback(question=doc["question"], feedback=feedback)

            #     st.write("inside")
                    # else:
                    #     st.subheader("Feedback")
                    #     st.write(doc["feedback"])
                        #st.write(doc["answer"])

        # with st.expander(label="Q2", expanded=(st.session_state.current_idx==2)):
        #     st.session_state.current_idx = 2
        #     qa_template(page_idx=2)
        
        # recording_template(0)
        # st.session_state.current_idx = 2
        # recording_template(2)
        # question_template(page_idx=1)

