import typing
import pickle
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
    f"Choose yours {st.session_state.language} proficiency level",
    key="proficiency",
    options=["Beginner", "Intermediate", "Advanced"],
)
st.write(
    f"We're talking in {st.session_state.language} at the level of {st.session_state.proficiency}."
)
if (
    "language" in st.session_state
    and "proficiency" in st.session_state
    and "logfile" not in st.session_state
):  # ❗️TO-DO: file name w/ user unique ID
    st.session_state.logfile = "history.pickle"
    with open(st.session_state.logfile, "wb") as f:
        setting_prompt: typing.List[dict] = [
            {
                "role": "system",
                "content": f"Let's play role-play. Remember that I'm a Korean learning {st.session_state.language} and you are a fluent {st.session_state.language} speaker. My proficieny of {st.session_state.language} is {st.session_state.proficiency}. Let's say you work at a coffee shop and I am a client.",
            },
        ]
        pickle.dump(setting_prompt, f)

if "dialogue" not in st.session_state:
    st.session_state.dialogue = ""
st.write(st.session_state.dialogue)
st.text_input(r"👇", key="utterance", on_change=chat)
st.button("Quit", key="end_conversation", on_click=chat)
if "feedback" in st.session_state:
    st.write(st.session_state.feedback)
