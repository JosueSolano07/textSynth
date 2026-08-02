from pydantic import BaseModel


class DocumentResponse(BaseModel):

    id: str

    filename: str

    pages: int | None = None