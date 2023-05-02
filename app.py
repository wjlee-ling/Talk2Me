import typing
import pickle
import openai
import streamlit as st
from util.utils import *
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

# from chat import chat

openai.api_key = st.secrets["OPENAI_API_KEY"]
hide_pages(["interface"])

st.title("Talk 2 Me")
st.header("Tell me about yourself")
with st.form("setting"):
    st.subheader("Language")
    language = st.radio(
        "Choose a language to learn",
        key="language",
        options=["English", "Korean", "German"],
    )
    st.subheader("Situation")
    situation = st.radio(
        "Whare are you now?",
        key="situation",
        options=[
            "Starbucks",
            "AMC(movie theater)",
            "McDonald's",
            "Subway(restaurant)",
            "Zara",
        ],
    )
    st.subheader("Proficiency")
    proficiency = st.radio(
        f"Choose your {st.session_state.language} proficiency level",
        key="proficiency",
        options=["Beginner", "Intermediate", "Advanced"],
    )
    submitted = st.form_submit_button("Let's talk!")

if submitted:
    # setting_prompt: typing.List[dict] = [
    #             {
    #                 "role": "system",
    #                 "content": f"Let's play role-play. Remember that I'm a Korean learning {st.session_state.language} and you are a fluent {st.session_state.language} speaker.\
    #                 My proficieny of {st.session_state.language} is {st.session_state.proficiency}. Let's say you work at {st.session_state.situation} and I am a client.",
    #             },
    #         ]

    # log = load_history("log.pickle")
    # log.append({
    #     "language": st.session_state.language,
    #     "situation": st.session_state.situation,
    #     "proficiency": st.session_state.proficiency,
    # })
    # log.append(setting_prompt)
    # save_history("log.pickle", log)

    if "logfile" not in st.session_state:  # ❗️TO-DO: file name w/ user unique ID
        st.session_state.logfile = "log.pickle"
        with open(st.session_state.logfile, "wb") as f:
            setting_prompt: typing.List[dict] = [
                {
                    "language": st.session_state.language,
                    "situation": st.session_state.situation,
                    "proficiency": st.session_state.proficiency,
                },
                {
                    "role": "system",
                    "content": f"Let's play role-play. Remember that I'm a Korean learning {st.session_state.language} and you are a fluent {st.session_state.language} speaker.\
                    My proficieny of {st.session_state.language} is {st.session_state.proficiency}. Let's say you work at {st.session_state.situation} and I am a client.",
                },
            ]
            pickle.dump(setting_prompt, f)

    switch_page("interface")
