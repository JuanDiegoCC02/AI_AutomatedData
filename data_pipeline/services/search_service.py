from .vector_store import collection


def semantic_search(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    return results