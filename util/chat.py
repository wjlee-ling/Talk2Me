import typing
import pickle
import openai
import streamlit as st

from util.utils import *


engine = st.secrets.GPT_MODEL


def get_response(messages):
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
    )
    response = completion.choices[0].message.content
    return response


@st.cache_data
def get_feedback(question, answer):
    messages = [
        {
            "role": "system",
            "content": st.secrets["opic_interview_feedback_prompt"],
        },
        {
            "role": "user",
            "content": f"[Q] {question} [A] {answer}",
        },
    ]
    response = get_response(messages)
    return response
