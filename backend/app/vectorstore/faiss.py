from pathlib import Path
import pickle

import faiss
import numpy as np

from app.core.config import settings
from app.models.chunk import Chunk


class FaissVectorStore:
    """
    Almacén vectorial basado en FAISS.

    Guarda:
    - Índice FAISS
    - Metadatos de los Chunks
    """

    def __init__(self):

        self.index_path = Path(settings.VECTOR_FOLDER) / "index.faiss"
        self.meta_path = Path(settings.VECTOR_FOLDER) / "chunks.pkl"

        self.index = None
        self.chunks: list[Chunk] = []

        self._load()

    # ---------------------------------------------------------

    def _load(self):

        if self.index_path.exists():

            self.index = faiss.read_index(str(self.index_path))

        if self.meta_path.exists():

            with open(self.meta_path, "rb") as f:

                self.chunks = pickle.load(f)

    # ---------------------------------------------------------

    def _save(self):

        if self.index is not None:

            faiss.write_index(
                self.index,
                str(self.index_path),
            )

        with open(self.meta_path, "wb") as f:

            pickle.dump(self.chunks, f)

    # ---------------------------------------------------------

    def add(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ):

        if not embeddings:
            return

        vectors = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        if self.index is None:

            dimension = vectors.shape[1]

            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(vectors)

        self.chunks.extend(chunks)

        self._save()

    # ---------------------------------------------------------

    def search(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> list[Chunk]:

        if self.index is None:

            return []

        query = np.asarray(
            [embedding],
            dtype=np.float32,
        )

        distances, indices = self.index.search(query, k)

        results = []

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            chunk = self.chunks[idx]

            chunk.score = float(score)

            results.append(chunk)

        return results

    # ---------------------------------------------------------

    def clear(self):

        self.index = None

        self.chunks = []

        if self.index_path.exists():
            self.index_path.unlink()

        if self.meta_path.exists():
            self.meta_path.unlink()