import json
import streamlit as st

from datetime import datetime
from dataclasses import dataclass
from pymongo import MongoClient


@dataclass
class Database:
    user_id: str
    theme: str

    def __post_init__(self):
        client = MongoClient(st.secrets["mongo_uri"])
        self.db = client.get_database("opic")
        self.theme = self.theme.replace(" ", "_")

    @classmethod
    def init_database(cls, user_id, theme):
        return Database(user_id=user_id, theme=theme)

    def get_current_time(self):
        return datetime.now().strftime("%Y%m%d%H%M")

    def insert_one(self, collection, insertion: dict):
        assert collection in self.db.list_collection_names()
        insertion["theme"] = self.theme
        insertion["user_id"] = self.user_id
        insertion["time"] = self.get_current_time()
        insertion["collection"] = collection
        post_id = self.db[collection].insert_one(insertion).inserted_id

        return post_id

    def find_one(self, collection, hint: dict):
        assert collection in self.db.list_collection_names()
        hint["user_id"] = self.user_id
        hint["theme"] = self.theme
        hint["collection"] = collection

        return self.db[collection].find_one(hint)

    def update_document(self, collection, file_path):
        """
        Read updated local json file and reflect new changes to MongoDB server
        """
        with open(file_path, encoding="UTF-8") as f:
            json_object = json.load(f)
        # doc_id = json_object["_id"]
        response = self.db[collection].update_one(
            filter={"theme": json_object["theme"]},
            update={"$set": json_object},
            upsert=True,
        )

    def get_interview_questions(self, theme: str):
        hint = {"theme": theme}
        return self.db["questions"].find_one(hint)["questions"]

    def update_feedback(self, question, feedback):
        self.db["interviews"].update_one(
            filter={"user_id": self.user_id, "theme": self.theme, "question": question},
            update={"$set": {"feedback": feedback}},
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path")
    parser.add_argument("-c", "--collection", default="questions")
    args = parser.parse_args()

    database = Database(user_id="admin", theme="test")
    database.update_document(collection=args.collection, file_path=args.path)
