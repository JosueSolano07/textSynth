def rerank(matches):

    filtered = [
        m for m in matches
        if m.get("content") and len(m["content"].strip()) > 40
    ]

    if not filtered:
        return matches

    if not any(m.get("score") for m in filtered):
        return filtered

    return sorted(filtered, key=lambda x: x.get("score", 0), reverse=True)