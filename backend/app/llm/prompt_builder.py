class PromptBuilder:
    """
    Construye los prompts enviados al LLM.
    """

    SYSTEM_PROMPT = """
Eres TextSynth.

Responde utilizando únicamente el contexto proporcionado.

Si la información no aparece en el contexto, responde:

"No encontré esa información en los documentos disponibles."

Sé preciso, claro y evita inventar información.
""".strip()

    # ---------------------------------------------------------

    @classmethod
    def build_rag_prompt(
        cls,
        question: str,
        context: str,
    ) -> str:

        return f"""
{cls.SYSTEM_PROMPT}

========================
CONTEXTO
========================

{context}

========================
PREGUNTA
========================

{question}

========================
RESPUESTA
========================
""".strip()

    # ---------------------------------------------------------

    @classmethod
    def build_chat_messages(
        cls,
        question: str,
        context: str = "",
        history: list | None = None,
    ) -> list[dict]:

        messages = [

            {
                "role": "system",
                "content": cls.SYSTEM_PROMPT,
            }

        ]

        if history:

            for message in history:

                if (
                    isinstance(message, dict)
                    and "role" in message
                    and "content" in message
                ):

                    messages.append(

                        {
                            "role": message["role"],
                            "content": message["content"],
                        }

                    )

        if context:

            messages.append(

                {
                    "role": "system",
                    "content": f"Contexto:\n\n{context}",
                }

            )

        messages.append(

            {
                "role": "user",
                "content": question,
            }

        )

        return messages