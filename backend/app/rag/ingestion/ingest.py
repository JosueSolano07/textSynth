from pathlib import Path

from app.documents.parser import DocumentParser
from app.rag.ingestion.chunker import Chunker
from app.vectorstore.embeddings import EmbeddingManager
from app.vectorstore.faiss import FaissVectorStore


class IngestionPipeline:
    """
    Pipeline técnico encargado de transformar un archivo
    en conocimiento indexado.

    Flujo:

        Archivo
            │
            ▼
        Parser
            │
            ▼
        Documento
            │
            ▼
        Chunks
            │
            ▼
        Embeddings
            │
            ▼
        VectorStore
    """

    def __init__(self):

        self.parser = DocumentParser()

        self.chunker = Chunker()

        self.embedding_manager = EmbeddingManager()

        self.vectorstore = FaissVectorStore()

    async def ingest(self, file_path: str | Path) -> dict:

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(file_path)

        # -------------------------------------------------
        # 1. Leer documento
        # -------------------------------------------------

        document = self.parser.parse(file_path)

        # -------------------------------------------------
        # 2. Dividir en chunks
        # -------------------------------------------------

        chunks = self.chunker.split(document)

        # -------------------------------------------------
        # 3. Generar embeddings
        # -------------------------------------------------

        embeddings = self.embedding_manager.embed(chunks)

        # -------------------------------------------------
        # 4. Guardar en índice vectorial
        # -------------------------------------------------

        self.vectorstore.add(
            chunks=chunks,
            embeddings=embeddings,
        )

        # -------------------------------------------------

        return {

            "success": True,

            "filename": file_path.name,

            "chunks": len(chunks),

            "indexed": True,
        }