import pickle
from pathlib import Path


def load_history(filename):
    p = Path(filename)
    if not p.exists():
        p.mkdir(parents=True)
        return []

    with open(filename, "rb") as f:
        history = pickle.load(f)

    return history


def save_history(filename, history):
    with open(filename, "wb") as f:
        pickle.dump(history, f)


# def get_new_queries():
#     import datetime
#     with open("last_seen_query.txt", "r") as f:
#         last_date_time = f.readline().strip()
#     logs = load_history("log.pickle")
