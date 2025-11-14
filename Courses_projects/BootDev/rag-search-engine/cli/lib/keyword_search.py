from .inverted_index import InvertedIndex
from .search_utils import (
    DEFAULT_SEARCH_LIMIT,
    process,
    load_stopwords,
)


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    stopwords = load_stopwords()
    tokens = process(query, stopwords)
    inv_index = InvertedIndex()

    try:
        inv_index.load()
    except FileNotFoundError as e:
        print(f"Index not found. Please run the build command first. - Error{e}")
        return []

    results: list[dict] = []
    seen_ids: set[int] = set()

    for tk in tokens:
        doc_ids = inv_index.get_document(tk)
        for id in doc_ids:
            if id in seen_ids:
                continue
            seen_ids.add(id)
            results.append(inv_index.docmap[id])

            if len(results) >= limit:
                return results
    return results
