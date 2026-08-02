import requests


class OllamaProvider:
    """
    Proveedor de Ollama.

    Requiere que Ollama esté ejecutándose localmente:
        ollama serve
    """

    def __init__(
        self,
        model: str = "llama3.1:8b",
        base_url: str = "http://localhost:11434",
    ):

        self.model = model

        self.base_url = base_url.rstrip("/")

    # ---------------------------------------------------------

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        **kwargs,
    ) -> str:

        response = requests.post(

            f"{self.base_url}/api/generate",

            json={

                "model": self.model,

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": temperature,

                },

            },

            timeout=300,

        )

        response.raise_for_status()

        return response.json()["response"]

    # ---------------------------------------------------------

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        **kwargs,
    ) -> str:

        response = requests.post(

            f"{self.base_url}/api/chat",

            json={

                "model": self.model,

                "messages": messages,

                "stream": False,

                "options": {

                    "temperature": temperature,

                },

            },

            timeout=300,

        )

        response.raise_for_status()

        return response.json()["message"]["content"]

    # ---------------------------------------------------------

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = requests.post(

            f"{self.base_url}/api/embeddings",

            json={

                "model": "nomic-embed-text",

                "prompt": text,

            },

            timeout=300,

        )

        response.raise_for_status()

        return response.json()["embedding"]

    # ---------------------------------------------------------

    async def health(self) -> bool:

        try:

            response = requests.get(

                f"{self.base_url}/api/tags",

                timeout=5,

            )

            return response.status_code == 200

        except Exception:

            return False