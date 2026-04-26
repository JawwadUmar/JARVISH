
from typing import TypedDict

class DBItem(TypedDict):
    question: str
    normalized: str
    embedding: list[float]
    answer: str

def makeDBItem(question: str, answer: str)->DBItem:
    return {
        "question":question, 
            "normalized": normalize(question),
            "embedding": [], 
            "answer":answer
    }