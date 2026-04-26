import re
from app.database.db_record import DBItem

def normalize(text):
    text = text.lower()
    #Find every character that is not a lowercase letter, a digit, or a space, and replace it with nothing
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text.strip()


def exact_match(normalized_q:str, db: list[DBItem]) -> str|None:
    for item in db:
        if item["normalized"] == normalized_q:
            return item["answer"]
    return None


