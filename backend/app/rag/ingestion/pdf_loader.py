import pdfplumber
from app.utils.text import clean_text


def extract_pdf(path: str):
    pages = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            pages.append((i, clean_text(text)))

    return pages