from app.models.chunk import Chunk


class ChunkFilter:
    """
    Filtros aplicados después del retrieval y antes del LLM.
    """

    # ---------------------------------------------------------

    @staticmethod
    def remove_empty(
        chunks: list[Chunk],
    ) -> list[Chunk]:

        return [

            chunk

            for chunk in chunks

            if chunk.text.strip()

        ]

    # ---------------------------------------------------------

    @staticmethod
    def remove_duplicates(
        chunks: list[Chunk],
    ) -> list[Chunk]:

        seen = set()

        filtered = []

        for chunk in chunks:

            key = chunk.text.strip()

            if key in seen:
                continue

            seen.add(key)

            filtered.append(chunk)

        return filtered

    # ---------------------------------------------------------

    @staticmethod
    def min_length(
        chunks: list[Chunk],
        length: int = 50,
    ) -> list[Chunk]:

        return [

            chunk

            for chunk in chunks

            if len(chunk.text) >= length

        ]

    # ---------------------------------------------------------

    @classmethod
    def apply(
        cls,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        chunks = cls.remove_empty(chunks)

        chunks = cls.remove_duplicates(chunks)

        chunks = cls.min_length(chunks)

        return chunks