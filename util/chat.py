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


def get_feedback(doc):
    messages = [
        {
            "role": "system",
            "content": st.secrets["opic_interview_feedback_prompt"],
        },
        {
            "role": "user",
            "content": f"[Q] {doc['question']} [A] {doc['answer']}",
        },
    ]
    response = get_response(messages)
    return response
