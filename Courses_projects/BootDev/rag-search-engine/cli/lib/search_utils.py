import json
import os
import string
from nltk.stem import PorterStemmer

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOP_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")


def load_movies() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["movies"]


def load_stopwords() -> list[str]:
    with open(STOP_PATH, "r") as f:
        stopwords = f.readlines()
    return [w.strip() for w in stopwords if w]


table = str.maketrans("", "", string.punctuation)


def clean_word(word: str) -> str:
    word = word.lower()
    return word.translate(table)


def tokenize(text: str) -> list[str]:
    cleaned = clean_word(text)
    tokens = cleaned.split()
    return [t for t in tokens if t]


def tokens_match(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for q in query_tokens:
        for t in title_tokens:
            if q in t:
                return True
    return False


def remove_stopwords(word: list[str], stopwords: list[str]):
    out = []
    for w in word:
        if w not in stopwords:
            out.append(w)
        else:
            continue
    return out


stemmer = PorterStemmer()


def process(text: str, stopwords: list[str]) -> list[str]:
    out = tokenize(text)
    out = remove_stopwords(out, stopwords)
    return [stemmer.stem(w) for w in out]
