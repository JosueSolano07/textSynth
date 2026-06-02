from app.rag.ingestion.pdf_loader import extract_pdf
from app.rag.ingestion.chunker import chunk_text
from app.rag.ingestion.embedder import embed_text

from app.rag.retrieval.vector_search import search_vectors
from app.rag.retrieval.reranker import rerank

from app.services.llm_service import generate_answer
from app.db.queries import insert_chunks


def ingest_document(path: str):
    pages = extract_pdf(path)

    batch = []
    inserted = 0

    for page_index, text in pages:

        chunks = chunk_text(text)

        for chunk_index, chunk in enumerate(chunks):

            embedding = embed_text(chunk)

            batch.append({
                "content": chunk,
                "embedding": embedding,
                "page": page_index,
                "chunk_index": chunk_index
            })

            inserted += 1

    insert_chunks(batch)

    return inserted


def ask_question(question: str):

    matches = search_vectors(question)

    filtered = rerank(matches)

    if not filtered:
        return {
            "question": question,
            "answer": "No se encontró información relevante en los documentos.",
            "sources": []
        }

    context = "\n\n".join([m["content"] for m in filtered])

    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": filtered
    }