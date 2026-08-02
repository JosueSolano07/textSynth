from pathlib import Path

from app.documents.loaders.pdf import PDFLoader
from app.documents.loaders.txt import TXTLoader
from app.documents.loaders.md import MarkdownLoader
from app.documents.loaders.doc import DocLoader
from app.documents.loaders.html import HTMLLoader


class LoaderFactory:
    """
    Devuelve el loader adecuado según la extensión del archivo.
    """

    def __init__(self):

        self.loaders = {
            ".pdf": PDFLoader(),
            ".txt": TXTLoader(),
            ".md": MarkdownLoader(),
            ".docx": DocLoader(),
            ".doc": DocLoader(),
            ".html": HTMLLoader(),
            ".htm": HTMLLoader(),
        }

    # ---------------------------------------------------------

    def get_loader(self, file_path: str | Path):

        suffix = Path(file_path).suffix.lower()

        loader = self.loaders.get(suffix)

        if loader is None:

            supported = ", ".join(sorted(self.loaders.keys()))

            raise ValueError(
                f"Formato '{suffix}' no soportado. "
                f"Formatos válidos: {supported}"
            )

        return loader