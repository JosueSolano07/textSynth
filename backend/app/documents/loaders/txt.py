from pathlib import Path

from app.models.document import Document


class TXTLoader:
    """
    Loader para archivos de texto plano.
    """

    def load(
        self,
        file_path: str | Path,
    ) -> Document:

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return Document.from_file(
            file_path=path,
            text=text,
        )