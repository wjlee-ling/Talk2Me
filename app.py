import typing
import pickle
import random
import openai
import streamlit as st
from collections import defaultdict
from util.utils import *
from util.database import Database
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

openai.api_key = st.secrets["OPENAI_API_KEY"]
hide_pages(["question1", "question2", "question3"])

st.title("Talk")
st.header("Background Survey")
with st.form("setting"):
    # 서베이 예시 https://seul96.tistory.com/329
    st.subheader("What do you do for fun?")
    hobby = st.radio(
        "Choose one of the following",
        key="hobby",
        options=["Go to the movies", "Read books"],
    )

    submitted = st.form_submit_button("Start Test")

if submitted:
    db = Database.init_database(user_id="admin")
    
    if "questions" not in st.session_state:
        Q_go_movies = [
            "You indicated in the survey that you like to go to the movies. Can you describe the last movie you watched?",
            "Who is your favorite movie actor or actress? Tell me a specific story about something this actor did that you heard about in the news. Begins the story with some details about the actor or actress and then tell me all the detail of what happened.",
            "I'd like you to tell me about one of the most memorable movies you've seen. What is the story about? Who was the main actor or actress? How did the movie affect you?",
        ]
        st.session_state.questions = [""] + random.sample(Q_go_movies, 2)
        print(st.session_state.questions)
        st.session_state.answers = defaultdict(str)

    if "logfile" not in st.session_state:
        st.session_state.logfile = "log.pickle"
        # with open(st.session_state.logfile, "wb") as f:
    switch_page("question1")
 