import streamlit as st
from chat import chat
st.write(
    f"We're in {st.session_state['situation']}. Let's talk in {st.session_state.language} at the {st.session_state.proficiency} level."
)
if "dialogue" not in st.session_state:
    st.session_state.dialogue = ""
st.write(st.session_state.dialogue)
st.text_input(r"👇", key="utterance", on_change=chat)
st.button("Quit", key="end_conversation", on_click=chat)
if "feedback" in st.session_state:
    st.write(st.session_state.feedback)
