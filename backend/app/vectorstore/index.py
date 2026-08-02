from app.vectorstore.faiss import FaissVectorStore


class VectorStore:
    """
    Fachada del almacenamiento vectorial.

    El resto del proyecto nunca debe conocer
    qué backend vectorial se está utilizando.

    Ejemplo:

        Retriever
            ↓
        VectorStore
            ↓
        FAISS
    """

    def __init__(self):

        # Por ahora usamos FAISS.
        # Más adelante podrá elegirse desde Settings.
        self.backend = FaissVectorStore()

    # ---------------------------------------------------------

    def add(
        self,
        embeddings: list,
        metadata: list,
    ):

        return self.backend.add(
            embeddings=embeddings,
            metadata=metadata,
        )

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        return self.backend.search(
            query=query,
            top_k=top_k,
        )

    # ---------------------------------------------------------

    def save(self):

        return self.backend.save()

    # ---------------------------------------------------------

    def load(self):

        return self.backend.load()

    # ---------------------------------------------------------

    def clear(self):

        return self.backend.clear()