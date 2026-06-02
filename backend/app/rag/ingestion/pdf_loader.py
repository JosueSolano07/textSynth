import pdfplumber

def load_pdf(path: str, max_pages: int = 15):
    pages = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= max_pages:
                break

            text = page.extract_text()
            if text:
                pages.append({
                    "page": i,
                    "content": text
                })

    return pages