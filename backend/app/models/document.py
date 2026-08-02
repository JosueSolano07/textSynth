from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Document:
    """
    Representa un documento procesado dentro del ecosistema TextSynth.

    Es la entidad principal utilizada por:

    - Parser
    - Chunker
    - Embeddings
    - Retrieval
    - Gran Educador
    - IA Multimodal
    """

    # ---------------------------------------------------------
    # Identidad
    # ---------------------------------------------------------

    id: str | None = None

    filename: str = ""

    source: str = ""

    extension: str = ""

    # ---------------------------------------------------------
    # Contenido
    # ---------------------------------------------------------

    text: str = ""

    language: str | None = None

    # ---------------------------------------------------------
    # Metadatos
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Estadísticas
    # ---------------------------------------------------------

    pages: int = 0

    words: int = 0

    characters: int = 0

    chunks: int = 0

    # ---------------------------------------------------------
    # Utilidades
    # ---------------------------------------------------------

    @classmethod
    def from_file(
        cls,
        file_path: str | Path,
        text: str,
        metadata: dict | None = None,
    ):

        path = Path(file_path)

        metadata = metadata or {}

        return cls(

            filename=path.name,

            source=str(path),

            extension=path.suffix.lower(),

            text=text,

            metadata=metadata,

            words=len(text.split()),

            characters=len(text),

        )

    # ---------------------------------------------------------

    @property
    def is_empty(self):

        return len(self.text.strip()) == 0

    # ---------------------------------------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "filename": self.filename,

            "source": self.source,

            "extension": self.extension,

            "text": self.text,

            "language": self.language,

            "metadata": self.metadata,

            "pages": self.pages,

            "words": self.words,

            "characters": self.characters,

            "chunks": self.chunks,

        }