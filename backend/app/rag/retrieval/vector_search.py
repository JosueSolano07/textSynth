from app.db.supabase_client import supabase


def search_vectors(question_embedding, match_count=5):
    response = supabase.rpc("match_documents", {
        "query_embedding": question_embedding,
        "match_count": match_count * 5  # overfetch para rerank
    }).execute()

    results = response.data or []

    print("RAW RESULTS:", len(results))

    if not results:
        return []

    normalized = []

    # =========================
    # NORMALIZACIÓN ROBUSTA
    # =========================
    for r in results:

        # prioridad 1: similarity explícita
        if r.get("similarity") is not None:
            score = float(r["similarity"])

        # prioridad 2: score directo
        elif r.get("score") is not None:
            score = float(r["score"])

        # prioridad 3: distance pgvector
        elif r.get("distance") is not None:
            score = 1 - float(r["distance"])

        else:
            score = 0.0

        r["score"] = score
        normalized.append(r)

    # =========================
    # SORT por relevancia
    # =========================
    normalized.sort(key=lambda x: x["score"], reverse=True)

    # =========================
    # TAKE TOP K (antes de rerank)
    # =========================
    top_k = normalized[:match_count * 3]

    # =========================
    # DEDUP (más robusto)
    # =========================
    seen = set()
    unique = []

    for r in top_k:
        content = (r.get("content") or "").strip()

        if not content:
            continue

        key = content[:150].lower()

        if key in seen:
            continue

        if is_bad_chunk(content):
            continue

        seen.add(key)
        unique.append(r)

        if len(unique) >= match_count * 3:
            break

    return unique

def is_bad_chunk(text: str) -> bool:
    text = text.strip()

    if len(text) < 40:
        return True

    if text.count(" ") < 5:
        return True

    return False