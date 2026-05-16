from pydantic import BaseModel

class DocumentBase(BaseModel):
    filename: str
    content: str

class DocumentResponse(DocumentBase):
    id: int

    class Config:
        from_attributes = True