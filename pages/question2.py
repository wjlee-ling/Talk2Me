from util.templates import question_template

from util.chat import get_feedback
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript

import streamlit as st
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

page_idx = 2
# question_template(page_idx)

hide_idx = ["Question" + str(idx) for idx in range(page_idx + 1, st.session_state.db.n_questions + 1)]
hide_pages(hide_idx)
question_item = st.session_state.questions[page_idx]
question_content = question_item["question"]
question_type = question_item["type"]

st.subheader(f"Q{page_idx}. {question_content}")
wav_bytes = None
wav_bytes = get_mic_input()
if st.session_state.db.status[page_idx] and wav_bytes:
    path = Path(f"q{page_idx}.wav")
    if path.exists():
        path.unlink()
    with open(f"q{page_idx}.wav", mode="bx") as f:
        f.write(wav_bytes)
    audio = open(f"q{page_idx}.wav", "rb")
    transcript = get_transcript(audio)
    st.session_state.db.status[page_idx] = 1
    st.session_state.db.insert_one(
        collection="interviews",
        insertion={
            "question": question_content,
            "type": question_type,
            "answer": transcript,
            "feedback": "",
        },
    )
    del wav_bytes

doc = st.session_state.db.find_one(
    collection="interviews",
    hint={
        "question": question_content,
        "type": question_type,
    },
)

if doc and st.session_state.db.status[page_idx]:
    st.write(doc["answer"])

    if doc["feedback"] == "":
        feedback = get_feedback(doc)
        st.session_state.db.update_feedback(question=doc["question"], feedback=feedback)
    else:
        st.subheader("Feedback")
        st.write(doc["feedback"])

    if page_idx != st.session_state.db.n_questions:
        if st.button("next"):
            switch_page(f"Question{page_idx+1}")