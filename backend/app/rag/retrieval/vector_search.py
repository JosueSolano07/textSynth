from app.db.supabase_client import supabase


def search_vectors(question_embedding, match_count=5):

    response = supabase.rpc("match_documents", {
        "query_embedding": question_embedding,
        "match_count": match_count * 5
    }).execute()

    results = response.data or []

    if not results:
        return []

    normalized = []

    for r in results:

        if r.get("similarity") is not None:
            score = float(r["similarity"])

        elif r.get("score") is not None:
            score = float(r["score"])

        elif r.get("distance") is not None:
            score = 1 - float(r["distance"])

        else:
            score = 0.0

        # clamp
        score = max(0.0, min(1.0, score))

        r["score"] = score
        normalized.append(r)

    normalized.sort(key=lambda x: x["score"], reverse=True)

    top_k = normalized[:match_count * 3]

    seen = set()
    unique = []

    for r in top_k:

        content = (r.get("content") or "").strip()

        if is_bad_chunk(content):
            continue

        key = content[:150].lower()

        if key in seen:
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