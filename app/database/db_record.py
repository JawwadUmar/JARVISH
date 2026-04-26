
from typing import TypedDict
from app.utils.process_question import normalize

class DBItem(TypedDict):
    question: str
    normalized: str
    embedding: list[float]
    answer: str

def makeDBItem(normalized_question: str, answer: str)->DBItem:
    return {
            "question":normalized_question, 
            "normalized": normalized_question,
            "embedding": [], 
            "answer":answer
    }