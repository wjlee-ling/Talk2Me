import typing
import openai
import streamlit as st

from chat import chat

openai.api_key = st.secrets["OPENAI_API_KEY"]
engine = st.secrets.GPT_MODEL

st.title("Talk 2 Me")

st.sidebar.header("Tell me about yourself")
st.sidebar.subheader("Language")
language = st.sidebar.radio(
    "Choose a language to learn",
    key="language",
    options=["English", "Korean", "German"],
)
st.sidebar.subheader("Proficiency")
proficiency = st.sidebar.radio(
    f"CHoose yours {st.session_state.language} proficiency level",
    key="proficiency",
    options=["Beginner", "Intermediate", "Advanced"],
)
st.write(f"We're talking in {st.session_state.language} at the level of {st.session_state.proficiency}.")
if "dialogue" not in st.session_state:
    st.session_state.dialogue = ""
st.write(st.session_state.dialogue)
st.text_input(r"👇", key="utterance", on_change=chat)
