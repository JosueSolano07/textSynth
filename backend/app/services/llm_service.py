import requests
from app.domain.config import GROQ_API_KEY, GROQ_URL


def generate_answer(question: str, context: str):

    prompt = f"""
Eres un asistente experto en documentos.

Reglas:
- Responde SOLO usando el contexto.
- Si no está en el contexto, di: "No tengo información suficiente."
- Si el contexto es suficiente, explica de forma clara y completa.
- Si es corto, expande ligeramente sin inventar información.
- No repitas literalmente el texto.
- Usa lenguaje natural y educativo.

CONTEXTO:
{context}

PREGUNTA:
{question}
"""

    res = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        },
        timeout=60
    )

    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]