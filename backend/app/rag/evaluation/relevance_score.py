def relevance_score(chunk: str, query: str) -> float:
    """
    Score básico inicial de relevancia.
    Más adelante se reemplaza por cross-encoder o LLM reranker.
    """

    if not chunk or not query:
        return 0.0

    chunk_words = set(chunk.lower().split())
    query_words = set(query.lower().split())

    if not query_words:
        return 0.0

    overlap = chunk_words.intersection(query_words)

    return len(overlap) / len(query_words)