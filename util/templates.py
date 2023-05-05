from util.chat import chat
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript

import streamlit as st
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages


def question_template(page_idx):
    hide_idx = ["Question"+str(idx) for idx in range(page_idx+1, st.session_state.n_questions+1)]
    hide_pages(hide_idx)
    st.subheader(f"Q{page_idx}. {st.session_state.questions[page_idx]}")

    wav_bytes = get_mic_input()
    if wav_bytes:
        path = Path(f"q{page_idx}.wav")
        if path.exists():
            path.unlink()
        with open(f"q{page_idx}.wav", mode="bx") as f:
            f.write(wav_bytes)
        audio = open(f"q{page_idx}.wav", "rb")
        transcript = get_transcript(audio)
        st.session_state.db.insert_one(
            collection = "interviews",
            insertion = {
            "question" : st.session_state.questions[page_idx],
            "answer" : transcript,
            }
        )
        del wav_bytes

    doc = st.session_state.db.find_one(
        collection="interviews",
        hint={"question":st.session_state.questions[page_idx]},
        )

    if doc and "answer" in doc:
        st.write(doc["answer"])
        if page_idx != st.session_state.n_questions: 
            if st.button("next"):
                switch_page(f"Question{page_idx+1}")