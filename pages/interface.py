import streamlit as st
from util.chat import chat
from util.utils import *

st.session_state.logfile = "log.pickle"
log = load_history(st.session_state.logfile)
st.session_state.situation, st.session_state.language, st.session_state.proficiency = (
    log[0]["situation"],
    log[0]["language"],
    log[0]["proficiency"],
)

st.write(
    f"We're in {st.session_state.situation}. Let's talk in {st.session_state.language} at the {st.session_state.proficiency} level."
)
if "dialogue" not in st.session_state:
    st.session_state.dialogue = ""
st.write(st.session_state.dialogue)
st.text_input(r"👇", key="utterance", on_change=chat)
st.button("Quit", key="end_conversation", on_click=chat)
if "feedback" in st.session_state:
    st.write(st.session_state.feedback)
