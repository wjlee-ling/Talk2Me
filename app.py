import os
import time
import typing
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
engine = st.secrets.GPT_MODEL

st.title("Talk 2 Me")

st.header("Let's get to know.")

st.subheader("Language")
language = st.radio(
    "Choose a language to learn",
    options=["English", "Korean", "German"],
)

st.subheader("Proficiency")
proficiency = st.radio(
    f"Your {language} proficiency level",
    options=["Beginner", "Intermediate", "Advanced"],
)


def input_prmpt(messages: typing.List[dict]) -> str:
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
    )
    return completion.choices[0].message.content


# Define a function to prompt the user for input and generate a response
def chat():
    messages: typing.List[dict] = [
        {
            "role": "system",
            "content": f"Let's play role-play. Remember that I'm a Korean learning {language} and you are a fluent {language} speaker.\
            My proficieny of {language} is {proficiency}. Let's say you work at a coffee shop and I am a client.",
        },
        {"role": "user", "content": "Hi"},
    ]

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

        # if st.button(label="End Conversation", on_click=True, key=turns*12345):
        #     break

    if prompt != "":
        correction = correct(messages)
        st.write(f"Bot: Here is my advice for you.\n{correction}")


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
