import streamlit as st

from datetime import datetime
from dataclasses import dataclass, field, InitVar
from pymongo import MongoClient


@dataclass
class Database:
    user_id: str
    theme: str
    # db:InitVar = field(init=False)

    def __post_init__(self):
        client = MongoClient(st.secrets["mongo_uri"])
        self.db = client.get_database("opic")

    @classmethod
    def init_database(cls, user_id, theme):
        return Database(user_id=user_id, theme=theme)
    
    def get_current_time(self):
        return datetime.now()
    
    def insert_one(self, collection, insertion:dict):
        assert collection in self.db.list_collection_names()
        insertion["theme"] = self.theme
        insertion["user_id"] = self.user_id
        insertion["time"] = self.get_current_time
        insertion["collection"] = collection
        post_id = self.db[collection].insert_one(insertion).inserted_id

        return post_id

    def find_one(self, collection, hint:dict):
        hint["user_id"] = self.user_id
        hint["theme"] = self.theme
        hint["collection"] = collection

        return self.db[collection].find_one(hint)