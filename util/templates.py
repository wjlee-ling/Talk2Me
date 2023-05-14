from util.chat import get_feedback
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript
import typing
import streamlit as st
from streamlit import session_state as sst


def qa_template(page_idx: int):
    question_item = sst.questions[page_idx]
    question_content = question_item["question"]
    question_type = question_item["type"]
    audio_file_name = f"{sst.db.user_id}_Q{page_idx}.wav"

    def _record(page_idx, wav_bytes):
        sst["answers"][page_idx]["wav"] = wav_bytes
        path = Path(audio_file_name)
        if path.exists():
            path.unlink()
        with open(audio_file_name, mode="bx") as f:
            f.write(wav_bytes)
        audio = open(audio_file_name, "rb")
        sst["answers"][page_idx]["transcript"] = get_transcript(audio)

        sst.db.insert_one(
            collection="interviews",
            insertion={
                "question": question_content,
                "type": question_type,
                "answer": sst["answers"][page_idx]["transcript"],
                "feedback": "",
                "audio": wav_bytes,
            },
        )
        st.experimental_rerun()

    def _update_feedback(page_idx: int, doc: dict):
        question, answer = doc["question"], doc["answer"]
        feedback = get_feedback(question, answer)
        sst.db.update_feedback(_item_id=doc["_id"], question=question, feedback=feedback)
        sst["answers"][page_idx]["id"] = doc["_id"]
        sst["answers"][page_idx]["feedback"] = feedback

    st.subheader(question_content)
    doc = sst.db.find_latest(
        collection="interviews",
        hint={
            "question": question_content,
            "type": question_type,
        },
    )
    wav_bytes = get_mic_input()
    if wav_bytes and doc is None:
        # first recording
        _record(page_idx, wav_bytes)

    elif doc is not None and wav_bytes and wav_bytes != sst["answers"][page_idx]["wav"]:
        # re-recording
        _record(page_idx, wav_bytes)

    elif doc is not None:
        # display user answer
        st.write(doc["answer"])

        if st.button("Next", key=f"next_button_{sst.current_idx}"):
            _update_feedback(page_idx, doc)

            # if sst.current_idx == sst.db.n_questions: # To-do : n_themes * n_questions
            #     # redirect to feedback page
            #     feedback_template(page_idx)
            # else:
            sst.current_idx += 1
            st.experimental_rerun()


@st.cache_data
def feedback_template(page_idx):
    def _format_feedback(question, answer, feedback):
        formatted = f"""
        **Q. {question}**\n
        A. {answer}\n
        [Feedback]\n
        {feedback}\n\n
        """
        return formatted

    feedback_combined = ""
    for idx in range(1, page_idx):
        question = sst["questions"][idx]["question"]
        answer = sst["answers"][idx]["transcript"]
        feedback = sst["answers"][idx]["feedback"].replace("[Q]", "").replace("[A]", "").strip().replace("  ", " ")
        feedback_combined += _format_feedback(question, answer, feedback)

    print(feedback_combined)
    st.write(feedback_combined)
