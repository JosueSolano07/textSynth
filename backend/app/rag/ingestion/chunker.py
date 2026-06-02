def chunk_text(text: str, max_words=120, overlap=20):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + max_words]))
        i += max_words - overlap

    return chunks