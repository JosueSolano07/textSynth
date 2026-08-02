from app.rag.pipeline import RAGPipeline


class RAGService:
    """
    Servicio de alto nivel para interactuar con el RAG.

    Expone operaciones de:
    - Ingesta
    - Recuperación
    - Construcción de contexto
    """

    def __init__(self):

        self.pipeline = RAGPipeline()

    # ---------------------------------------------------------

    async def ingest(
        self,
        file_path: str,
    ) -> dict:

        return self.pipeline.ingest(file_path)

    # ---------------------------------------------------------

    async def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        return self.pipeline.retrieve(
            question=question,
            top_k=top_k,
        )

    # ---------------------------------------------------------

    async def build_context(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        return self.pipeline.build_context(
            question=question,
            top_k=top_k,
        )

    # ---------------------------------------------------------

    async def clear(self):

        self.pipeline.vectorstore.clear()

        return {
            "success": True,
            "message": "Índice vectorial eliminado."
        }