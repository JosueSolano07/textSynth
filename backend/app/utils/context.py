def build_context(chunks, max_chars=2500):
    context = ""
    used = 0

    for c in chunks:
        text = (c.get("content") or "").strip()
        if not text:
            continue

        if used + len(text) > max_chars:
            break

        context += text + "\n\n"
        used += len(text)

    return context.strip()


def clean_sources(chunks):
    seen = set()
    cleaned = []

    for c in chunks:
        content = (c.get("content") or "").strip()
        if not content:
            continue

        cid = c.get("id", "no-id")

        key = (cid, content[:120].lower())

        if key in seen:
            continue

        seen.add(key)

        cleaned.append({
            "id": cid,
            "content": content,
            "score": round(float(c.get("score", 0) or 0), 4),
            "page": c.get("page"),
            "document_name": c.get("document_name")
        })

    return cleaned