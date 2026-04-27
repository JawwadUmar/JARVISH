
from typing import TypedDict
from app.utils.process_question import normalize

class DBItem(TypedDict):
    question: str
    normalized: str
    embedding: list[float]
    answer: str

def makeDBItem(question: str, normalized_question: str, answer: str)->DBItem:
    return {
            "question":question, 
            "normalized": normalized_question,
            "embedding": [], 
            "answer":answer
    }