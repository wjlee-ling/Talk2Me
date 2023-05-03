from util.chat import chat
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

# @st.cache_data(experimental_allow_widgets=True)
def question_template(page_idx):
    # hide_idx = ["question"+str(idx) for idx in range(1, page_idx)]
    # hide_pages(hide_idx)
    st.subheader(f"Q{page_idx}. {st.session_state.questions[page_idx]}")

    path = Path(f"q{page_idx}.wav")
    if not path.exists():
        wav_bytes = get_mic_input()
        if wav_bytes:
            with open(f"q{page_idx}.wav", mode="bx") as f:
                f.write(wav_bytes)
            audio = open(f"q{page_idx}.wav", "rb")
            transcript = get_transcript(audio)
            st.session_state.answers[page_idx] = transcript

    if st.session_state.answers[page_idx] != "":
        st.write(st.session_state.answers[page_idx])
        if page_idx != 2: 
            if st.button("next"):
                switch_page(f"question{page_idx+1}")