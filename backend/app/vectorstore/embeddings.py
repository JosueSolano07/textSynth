from typing import Iterable

from app.models.chunk import Chunk


class EmbeddingManager:
    """
    Genera embeddings para una lista de Chunks.

    El proveedor (Ollama, OpenAI, HuggingFace, etc.)
    podrá cambiar sin afectar el resto del sistema.
    """

    def __init__(self, provider=None):

        self.provider = provider

    # ---------------------------------------------------------

    def embed(
        self,
        chunks: Iterable[Chunk],
    ) -> list[list[float]]:

        embeddings = []

        for chunk in chunks:

            vector = self.embed_text(chunk.text)

            chunk.embedding = vector

            embeddings.append(vector)

        return embeddings

    # ---------------------------------------------------------

    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        if self.provider is None:
            raise NotImplementedError(
                "No hay proveedor de embeddings configurado."
            )

        return self.provider.embed(text)