import typing
import pickle
import openai
import streamlit as st

engine = st.secrets.GPT_MODEL
# Define a function to prompt the user for input and generate a response


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

    with open("history.pickle", "wb") as f:
        pickle.dump(messages, f)


def chat():
    with open("history.pickle", "rb") as f:
        messages = pickle.load(f)

    messages.append(
        {
            "role": "user",
            "content": st.session_state.utterance,
        }
    )
    get_response(messages)
    build_dialogue()


def correct(messages: typing.List[dict]):
    correction_request = {
        "role": "assistant",
        "content": "Could you give me feedback about my English in Korean?",
    }
    messages.append(correction_request)
    response = get_response(messages)
    return response


def build_dialogue():
    dialogue = []
    with open("history.pickle", "rb") as f:
        messages = pickle.load(f)

    for turn in messages:
        role, content = turn["role"], turn["content"]
        if role == "system":
            # do not display initial prompt setting
            continue
        elif role == "assistant":  # different bot names for different situations
            role = "bot"
        dialogue.append(f"{role}: {content}")

    st.session_state.dialogue = "\n\n".join(dialogue)
