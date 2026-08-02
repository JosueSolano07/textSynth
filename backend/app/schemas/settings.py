from pydantic import BaseModel


class SettingsResponse(BaseModel):

    llm_provider: str

    embedding_model: str

    reranker: str