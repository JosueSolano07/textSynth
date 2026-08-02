from app.llm.providers.ollama import OllamaProvider


class LLMManager:
    """
    Administrador de modelos LLM.

    Centraliza el acceso al proveedor configurado
    (Ollama, OpenAI, Gemini, Groq, etc.).
    """

    def __init__(self, provider=None):

        self.provider = provider or OllamaProvider()

    # ---------------------------------------------------------

    async def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        return await self.provider.generate(
            prompt=prompt,
            **kwargs,
        )

    # ---------------------------------------------------------

    async def chat(
        self,
        messages: list[dict],
        **kwargs,
    ) -> str:

        return await self.provider.chat(
            messages=messages,
            **kwargs,
        )

    # ---------------------------------------------------------

    async def embed(
        self,
        text: str,
    ):

        return await self.provider.embed(text)

    # ---------------------------------------------------------

    @property
    def name(self):

        return self.provider.__class__.__name__