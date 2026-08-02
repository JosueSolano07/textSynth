from pathlib import Path

from docx import Document as DocxDocument

from app.models.document import Document


class DocLoader:
    """
    Loader para documentos DOC y DOCX.
    """

    def load(
        self,
        file_path: str | Path,
    ) -> Document:

        path = Path(file_path)

        doc = DocxDocument(str(path))

        paragraphs = []

        for paragraph in doc.paragraphs:

            text = paragraph.text.strip()

            if text:

                paragraphs.append(text)

        full_text = "\n".join(paragraphs)

        metadata = {
            "author": doc.core_properties.author or "",
            "title": doc.core_properties.title or "",
            "subject": doc.core_properties.subject or "",
            "category": doc.core_properties.category or "",
            "keywords": doc.core_properties.keywords or "",
            "comments": doc.core_properties.comments or "",
        }

        document = Document.from_file(
            file_path=path,
            text=full_text,
            metadata=metadata,
        )

        document.pages = 1

        return document