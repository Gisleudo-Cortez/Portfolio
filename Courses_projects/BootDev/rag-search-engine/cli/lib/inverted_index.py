from lib.search_utils import process, load_stopwords, load_movies
import pickle
import os

stopwords = load_stopwords()
movies = load_movies()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
INDEX_PATH = os.path.join(CACHE_DIR, "index.pkl")
DOCMAP_PATH = os.path.join(CACHE_DIR, "docmap.pkl")


class InvertedIndex:
    def __init__(self) -> None:
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}

    def __add_document(self, doc_id, text) -> None:
        words = process(text, stopwords)
        for w in words:
            self.index.setdefault(w, set())
            self.index[w].add(doc_id)

    def get_document(self, term: str) -> list[int]:
        t = process(term, stopwords)
        out = set()
        for w in t:
            ids = self.index.get(w, set())
            out = out.union(ids)
        return sorted(out)

    def build(self) -> None:
        for m in movies:
            id = m["id"]
            doc = f"{m['title']} {m['description']}"
            self.__add_document(id, doc)
            self.docmap[id] = m

    def save(self) -> None:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(INDEX_PATH, "wb") as idx:
            pickle.dump(self.index, idx)
        with open(DOCMAP_PATH, "wb") as dm:
            pickle.dump(self.docmap, dm)

    def load(self) -> None:
        if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCMAP_PATH):
            raise FileNotFoundError(
                "Inverted index not found; run the build command first."
            )
        with open(INDEX_PATH, "rb") as f:
            self.index = pickle.load(f)
        with open(DOCMAP_PATH, "rb") as f:
            self.docmap = pickle.load(f)
