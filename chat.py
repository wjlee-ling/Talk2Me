import typing
import pickle
import openai
import streamlit as st

engine = st.secrets.GPT_MODEL
# Define a function to prompt the user for input and generate a response


def chat():
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)

    if st.session_state.end_conversation:
        get_feedback()
    else:
        messages.append(
            {
                "role": "user",
                "content": st.session_state.utterance,
            }
        )
        st.session_state.utterance = ""
        get_response(messages)
        build_dialogue()


def get_response(messages):
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
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
        "content": f"Could you give me feedback about my {st.session_state.language} in Korean considering my {st.session_state.language} proficiency is {st.session_state.proficiency}? Correct me in details if i was wrong.",
    }
    messages.append(feedback_request)
    get_response(messages)


def build_dialogue():
    dialogue = []
    with open(st.session_state.logfile, "rb") as f:
        messages = pickle.load(f)

    for turn in messages:
        role, content = turn["role"], turn["content"]
        if role == "system":
            # do not display initial prompt setting
            continue
        elif role == "assistant":  # different bot names for different situations
            role = "bot "
        dialogue.append(f"{role}: {content}")

    st.session_state.dialogue = "\n\n".join(dialogue)
