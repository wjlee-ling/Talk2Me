from util.chat import get_feedback
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript


import streamlit as st
from datetime import datetime
from streamlit import session_state as sst
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages


# @st.cache_resource(experimental_allow_widgets=True)
def qa_template(page_idx):
    question_item = sst.questions[page_idx]
    question_content = question_item["question"]
    question_type = question_item["type"]
    audio_file_name = f"{sst.db.user_id}_Q{page_idx}.wav"

    st.subheader(question_content)

    wav_bytes = get_mic_input()
    print("======================")
    print(st.session_state.current_idx)
    if wav_bytes:
        sst["answers"][page_idx]["wav"] = wav_bytes
        path = Path(audio_file_name)
        if path.exists():
            path.unlink()
        with open(audio_file_name, mode="bx") as f:
            f.write(wav_bytes)
        audio = open(audio_file_name, "rb")
        sst["answers"][page_idx]["transcript"] = get_transcript(audio)

        st.session_state.db.insert_one(
            collection="interviews",
            insertion={
                "question": question_content,
                "type": question_type,
                "answer": sst["answers"][page_idx]["transcript"],
                "feedback": "",
            },
        )

    doc = st.session_state.db.find_one(
        collection="interviews",
        hint={
            "question": question_content,
            "type": question_type,
        },
    )
    if doc and "answer" in doc:
        st.write(doc["answer"])

    # if doc and "answer" in doc:

    #     if st.button("Get Feedback", key=f"feedback_button_{sst.current_idx}"):
    #         if doc["feedback"] == "":
    #             feedback = get_feedback(doc)
    #             st.write(feedback)
    #             sst.db.update_feedback(question=doc["question"], feedback=feedback)
    #         else:
    #             st.subheader("Feedback")
    #             st.write(doc["feedback"])

