from app.models.chunk import Chunk


class Reranker:
    """
    Reordena los chunks recuperados.

    Actualmente utiliza la puntuación devuelta por
    FAISS. Más adelante podrá sustituirse por un
    CrossEncoder (BGE, Jina, Cohere, etc.).
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def rerank(
        self,
        question: str,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        if not chunks:
            return []

        return sorted(
            chunks,
            key=lambda chunk: chunk.score,
        )