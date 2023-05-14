from util.chat import get_feedback
from util.utils import *
from util.speech_to_text import get_mic_input, get_transcript
import time
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


@st.cache_data(experimental_allow_widgets=True)
def feedback_template(page_idx):
    def _format_feedback(question, answer, feedback):
        formatted = f"""
        **Q. {question}**\n
        A. {answer}\n
        [Feedback]\n
        {feedback}
        """
        return formatted

    feedback_ls = []
    for idx in range(1, page_idx):
        question = sst["questions"][idx]["question"]
        answer = sst["answers"][idx]["transcript"]
        feedback = sst["answers"][idx]["feedback"].replace("[Q]", "").replace("[A]", "").strip().replace("  ", " ")
        feedback_ls.append(_format_feedback(question, answer, feedback))

    st.subheader("💁‍♀️Ava thinks...")
    feedback = "\n".join(feedback_ls)
    st.write(feedback)
    if sst.user_feedback == "first_run":
        time.sleep(10.0)
        sst.user_feedback = "not_yet"
        st.experimental_rerun()
    elif sst.user_feedback == "sent":
        st.download_button(label="Download the feedback", data=feedback)  # file_name=f"Talk2Ava_{sst.username}.txt"
        if st.button(label="Talk 2 Ava **again**!"):
            sst.db.client.close()
            st.cache_resource.clear()
            st.experimental_rerun()


def user_feedback_template(page_idx):
    satisfaction_mapping = {"😍": "I'd looove to Talk2Ava!", "🤔": "I'm not sure.", "🙁": "Meh... Could be a lot better."}
    st.info("Wait! If you want to know how Ava thinks about your answers to the other questions, let me know how you like Talk2Ava💁‍♀️!")
    st.subheader("User Feedback")
    satisfaction = st.selectbox(
        "Satisfaction",
        ["😍", "🤔", "🙁"],
    )
    st.write("You've selected", satisfaction, f"({satisfaction_mapping[satisfaction]})")

    user_comment = st.text_input(label=f"Why {satisfaction}?", value="답변이 보다...")
    if user_comment == "답변이 보다..." or len(user_comment) < 5:
        st.warning("Want to hear more from you!")

    elif satisfaction and user_comment:
        sst.user_feedback = "sent"
        st.experimental_rerun()
