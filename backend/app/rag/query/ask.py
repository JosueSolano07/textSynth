from app.rag.retrieval.vector_search import search_vectors
from app.rag.retrieval.reranker import rerank
from app.rag.ingestion.embedder import embed_text
from app.services.llm_service import generate_answer
from app.utils.context import build_context, clean_sources


def ask_question(question: str):

    query_embedding = embed_text(question)

    # 1. retrieval
    matches = search_vectors(query_embedding)

    if not matches:
        return {
            "answer": "No se encontró información relevante.",
            "sources": []
        }

    # 2. rerank
    matches = rerank(matches)

    # fallback safety
    if not matches:
        matches = search_vectors(query_embedding)

    # 3. sources
    unique_sources = clean_sources(matches)

    # 4. context (LIMITADO)
    context = build_context(unique_sources, max_chars=2500)

    # 5. LLM
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": unique_sources
    }