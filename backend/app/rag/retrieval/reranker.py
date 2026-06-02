def rerank(matches):
    filtered = [
        m for m in matches
        if m.get("content") and len(m["content"].strip()) > 30
    ]

    # si no hay scores válidos, no romper orden
    if not any(m.get("score") for m in filtered):
        return filtered

    return sorted(filtered, key=lambda x: x.get("score", 0), reverse=True)