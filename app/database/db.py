import json

relative_db_path = "../../data/db.json"

def load_db():
    with open(relative_db_path, "r") as f:
        return json.load(f)

def save_to_db(data):
    with open(relative_db_path, "w") as f:
        json.dump(data, f)