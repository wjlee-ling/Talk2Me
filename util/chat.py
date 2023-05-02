import typing
import pickle
import openai
import streamlit as st

from util.utils import *

engine = st.secrets.GPT_MODEL


def chat():
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)

    if st.session_state.end_conversation:
        get_feedback()
        show_feedback()
    else:
        messages.append(
            {
                "role": "user",
                "content": st.session_state.utterance,
            }
        )
        st.session_state.utterance = ""
        get_response(messages)
        show_dialogue()


def get_response(messages):
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=messages[1:],
    )
    response = completion.choices[0].message.content
    newitem = {
        "role": "assistant",
        "content": response,
    }
    messages.append(newitem)

    with open(st.session_state.logfile, "wb") as f:
        pickle.dump(messages, f)


def get_feedback():
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)
    feedback_request = {
        "role": "assistant",
        "content": f"Given the past dialogue, could you give feedback in Korean about the user's (not assistant's) {st.session_state.language} considering his {st.session_state.language} proficiency is {st.session_state.proficiency}? Correct user's mistake in details if there is any.",
    }
    messages.append(feedback_request)
    get_response(messages)


def show_dialogue():
    dialogue = []
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)

    for turn in messages[1:]:
        role, content = turn["role"], turn["content"]
        if role == "system":
            # do not display initial prompt setting
            continue
        elif role == "assistant":  # different bot names for different situations
            role = ":robot_face:"
        elif role == "user":
            role = ":loudspeaker:"
        dialogue.append(f"{role}: {content}")

    st.session_state.dialogue = "\n\n".join(dialogue)


def show_feedback():
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)

    st.session_state.feedback = messages[-1]["content"]
