def rerank(matches):
    return [
        m for m in matches
        if m.get("content") and len(m["content"]) > 30
    ]