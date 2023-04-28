import os
import time
import typing
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
engine = st.secrets.GPT_MODEL
messages: typing.List[dict] = [
    {
        "role": "system",
        "content": "Let's play role-play. Remember that I'm a Korean learning English and you are a fluent English speaker. Let's say you work at a coffee shop and I am a client.",
    },
    {"role": "user", "content": "Hi"},
]

st.title("Learn English")


def input_prmpt(messages: typing.List[dict]) -> str:
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
    )
    return completion.choices[0].message.content


# Define a function to prompt the user for input and generate a response
def chat():
    turns = 0
    prompt = st.text_input(label="You: ", key=turns)
    st.write(f"You: {prompt}")
    turns = 0
    while len(prompt) > 0 and prompt != "quit":
        if turns == 7:
            break
        turns += 1
        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        response = input_prmpt(messages)
        st.write("Bot: ", response)
        messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        prompt = st.text_input(label="You: ", key=turns)
        st.write(f"You: {prompt}")
        time.sleep(0.58)
    if prompt == "quit":
        correction = correct(messages)
        st.write(f"Here is my advice for you:\n{correction}")


def correct(messages):
    correction_request = {
        "role": "assistant",
        "content": "Could you give me feedback about my English in Korean?",
    }
    messages.append(correction_request)
    response = input_prmpt(messages)
    return response


# Run the chatbot with a specific model
chat()
