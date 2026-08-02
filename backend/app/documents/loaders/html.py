from pathlib import Path

from bs4 import BeautifulSoup

from app.models.document import Document


class HTMLLoader:
    """
    Loader para documentos HTML.
    """

    def load(
        self,
        file_path: str | Path,
    ) -> Document:

        path = Path(file_path)

        html = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(html, "html.parser")

        # Eliminar elementos que no aportan contenido
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        # Limpiar líneas vacías
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        clean_text = "\n".join(lines)

        metadata = {
            "title": soup.title.string.strip()
            if soup.title and soup.title.string
            else "",
            "format": "html",
        }

        return Document.from_file(
            file_path=path,
            text=clean_text,
            metadata=metadata,
        )