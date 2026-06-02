import requests
from app.domain.config import GROQ_API_KEY, GROQ_URL


def generate_answer(question: str, context: str, history: list = None):

    # 1. construir historial en texto
    history_text = ""

    if history:
        for msg in history[-8:]:
            role = "Usuario" if msg.role == "user" else "Asistente"
            content = msg.content
            history_text += f"{role}: {content}\n"

    # 2. prompt estructurado tipo ChatGPT
    prompt = f"""
Eres un asistente inteligente con memoria de conversación.

REGLAS IMPORTANTES:
- Usa el historial para entender contexto personal del usuario
- Si el usuario pregunta "como me llamo", usa el historial
- Si no hay información suficiente, dilo de forma natural
- No inventes datos que no estén en el historial o contexto
- Responde de forma conversacional y clara

HISTORIAL DE CONVERSACIÓN:
{history_text if history_text else "No hay historial previo."}

CONTEXTO DE DOCUMENTOS:
{context if context else "Sin contexto relevante."}

PREGUNTA DEL USUARIO:
{question}
"""

    # 3. llamada al modelo
    res = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        },
        timeout=60
    )

    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]