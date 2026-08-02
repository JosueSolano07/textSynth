from pathlib import Path

from pypdf import PdfReader

from app.models.document import Document


class PDFLoader:
    """
    Loader para documentos PDF.
    """

    def load(
        self,
        file_path: str | Path,
    ) -> Document:

        path = Path(file_path)

        reader = PdfReader(str(path))

        pages = []
        metadata = {}

        if reader.metadata:

            metadata = {
                "title": reader.metadata.title or "",
                "author": reader.metadata.author or "",
                "creator": reader.metadata.creator or "",
                "producer": reader.metadata.producer or "",
                "subject": reader.metadata.subject or "",
            }

        for page in reader.pages:

            text = page.extract_text() or ""

            pages.append(text)

        full_text = "\n\n".join(pages)

        document = Document.from_file(
            file_path=path,
            text=full_text,
            metadata=metadata,
        )

        document.pages = len(reader.pages)

        return document