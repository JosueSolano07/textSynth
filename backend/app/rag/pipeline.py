from app.documents.parser import DocumentParser
from app.rag.ingestion.chunker import Chunker
from app.vectorstore.embeddings import EmbeddingManager
from app.vectorstore.faiss import FaissVectorStore

from app.rag.retrieval.retriever import Retriever
from app.rag.retrieval.reranker import Reranker
from app.rag.retrieval.filters import ChunkFilter


class RAGPipeline:
    """
    Pipeline principal de RAG.

    Ingesta:
        Archivo
            ↓
        Document
            ↓
        Chunks
            ↓
        Embeddings
            ↓
        FAISS

    Consulta:
        Pregunta
            ↓
        Embedding
            ↓
        Retriever
            ↓
        Reranker
            ↓
        Filters
            ↓
        Contexto
    """

    def __init__(self):

        self.parser = DocumentParser()

        self.chunker = Chunker()

        self.embedding_manager = EmbeddingManager()

        self.vectorstore = FaissVectorStore()

        self.retriever = Retriever()

        self.reranker = Reranker()

    # ---------------------------------------------------------

    def ingest(
        self,
        file_path: str,
    ):

        document = self.parser.parse(file_path)

        chunks = self.chunker.split(document)

        embeddings = self.embedding_manager.embed(chunks)

        self.vectorstore.add(
            chunks=chunks,
            embeddings=embeddings,
        )

        return {

            "document": document,

            "chunks": len(chunks),

            "success": True,

        }

    # ---------------------------------------------------------

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        chunks = self.retriever.retrieve(
            question=question,
            top_k=top_k,
        )

        chunks = self.reranker.rerank(
            question,
            chunks,
        )

        chunks = ChunkFilter.apply(chunks)

        return chunks

    # ---------------------------------------------------------

    def build_context(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        chunks = self.retrieve(
            question,
            top_k,
        )

        return "\n\n".join(

            chunk.text

            for chunk in chunks

        )