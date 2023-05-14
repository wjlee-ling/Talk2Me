import json
import streamlit as st

from datetime import datetime
from dataclasses import dataclass
from pymongo import MongoClient


@dataclass
class Database:
    user_id: str  # to be replaced w/ authentic user id
    theme: str
    n_questions: int
    session_time: str

    def __post_init__(self):
        self.client = MongoClient(st.secrets["mongo_uri"])
        self.db = self.client.get_database("opic")
        self.theme = self.theme.replace(" ", "_")

    def get_current_time(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    @st.cache_data
    def insert_one(self, collection, insertion: dict):
        print("DB: new insertion")
        assert collection in self.db.list_collection_names()
        insertion["theme"] = self.theme
        insertion["user_id"] = self.user_id
        insertion["submit_time"] = self.get_current_time()
        insertion["collection"] = collection
        insertion["session_time"] = self.session_time
        post_id = self.db[collection].insert_one(insertion).inserted_id

        return post_id

    def find_latest(self, collection, hint: dict):
        assert collection in self.db.list_collection_names()
        hint["user_id"] = self.user_id
        hint["theme"] = self.theme
        hint["collection"] = collection
        hint["session_time"] = self.session_time

        latest = self.db[collection].find(hint).sort("submit_time", -1).limit(1)
        try:
            return latest[0]
        except IndexError:
            return None

    def update_document(self, collection, file_path):
        """
        Read updated local json file and reflect new changes to MongoDB server
        """
        with open(file_path, encoding="UTF-8") as f:
            json_object = json.load(f)
        response = self.db[collection].update_one(
            filter={"theme": json_object["theme"]},
            update={"$set": json_object},
            upsert=True,
        )

    def get_interview_questions(self, theme: str):
        items = []
        for type in ["description", "experience", "habit", "comparison"]:
            results = self.db["questions"].aggregate(
                [
                    {"$unwind": "$items"},
                    {"$match": {"items.type": type}},
                    {"$sample": {"size": 1}},
                ]
            )
            for result in results:
                items.append(result["items"])
        return items

    @st.cache_data
    def update_feedback(self, _item_id, question, feedback):
        print("DB: add feedback")
        self.db["interviews"].update_one(
            filter={"_id": _item_id, "question": question},
            update={"$set": {"feedback": feedback}},
        )


@st.cache_resource
def init_database(user_id, theme, n_questions, session_time=None):
    print("DB: connected")
    if session_time is None:
        session_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return Database(user_id=user_id, theme=theme, n_questions=n_questions, session_time=session_time)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path")
    parser.add_argument("-c", "--collection", default="questions")
    args = parser.parse_args()

    database = Database(user_id="admin", theme="test")
    database.update_document(collection=args.collection, file_path=args.path)
