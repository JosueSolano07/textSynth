from app.models.chunk import Chunk
from app.vectorstore.embeddings import EmbeddingManager
from app.vectorstore.faiss import FaissVectorStore


class Retriever:
    """
    Recupera los Chunks más relevantes para una consulta.
    """

    def __init__(self):

        self.embedding_manager = EmbeddingManager()

        self.vectorstore = FaissVectorStore()

    # ---------------------------------------------------------

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[Chunk]:

        query_embedding = self.embedding_manager.embed_text(question)

        chunks = self.vectorstore.search(
            embedding=query_embedding,
            k=top_k,
        )

        return chunks