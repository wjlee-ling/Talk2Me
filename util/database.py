import streamlit as st

from dataclasses import dataclass, field, InitVar
from pymongo import MongoClient
from datetime import datetime


@dataclass
class Database:
    user_id:str 
    # db:InitVar = field(init=False)

    def __post_init__(self):
        client = MongoClient(st.secrets["mongo_uri"])
        self.db = client.get_database("opic")
    
    
    @classmethod
    def init_database(cls, user_id):
        return Database(user_id=user_id).db