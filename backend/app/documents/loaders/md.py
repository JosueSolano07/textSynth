from pathlib import Path

from app.models.document import Document


class MarkdownLoader:
    """
    Loader para archivos Markdown.
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

        metadata = {
            "format": "markdown",
        }

        return Document.from_file(
            file_path=path,
            text=text,
            metadata=metadata,
        )