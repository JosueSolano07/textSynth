from uuid import uuid4

from app.models.chunk import Chunk
from app.models.document import Document


class Chunker:
    """
    Divide un Document en múltiples Chunks.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    # ---------------------------------------------------------

    def split(
        self,
        document: Document,
    ) -> list[Chunk]:

        text = document.text.strip()

        if not text:
            return []

        chunks: list[Chunk] = []

        start = 0
        index = 0

        while start < len(text):

            end = min(start + self.chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    Chunk(
                        id=str(uuid4()),
                        document_id=document.id,
                        filename=document.filename,
                        source=document.source,
                        page=None,
                        index=index,
                        start=start,
                        end=end,
                        text=chunk_text,
                        metadata=document.metadata.copy(),
                    )
                )

                index += 1

            start += self.chunk_size - self.overlap

        document.chunks = len(chunks)

        return chunks