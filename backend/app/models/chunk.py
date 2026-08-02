from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    """
    Representa un fragmento de un documento.

    Es la unidad de trabajo del RAG.

    Todo el sistema de embeddings, retrieval,
    reranking y generación trabaja con Chunks.
    """

    # ---------------------------------------------------------
    # Identidad
    # ---------------------------------------------------------

    id: str

    document_id: str | None = None

    # ---------------------------------------------------------
    # Documento origen
    # ---------------------------------------------------------

    filename: str = ""

    source: str = ""

    page: int | None = None

    # ---------------------------------------------------------
    # Posición
    # ---------------------------------------------------------

    index: int = 0

    start: int = 0

    end: int = 0

    # ---------------------------------------------------------
    # Contenido
    # ---------------------------------------------------------

    text: str = ""

    # ---------------------------------------------------------
    # Información para Retrieval
    # ---------------------------------------------------------

    score: float = 0.0

    embedding: list[float] | None = None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------

    @property
    def length(self):

        return len(self.text)

    # ---------------------------------------------------------

    @property
    def words(self):

        return len(self.text.split())

    # ---------------------------------------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "document_id": self.document_id,

            "filename": self.filename,

            "source": self.source,

            "page": self.page,

            "index": self.index,

            "start": self.start,

            "end": self.end,

            "text": self.text,

            "score": self.score,

            "metadata": self.metadata,

        }