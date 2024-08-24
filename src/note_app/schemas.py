from pydantic import BaseModel


class NoteSchema(BaseModel):
    id: int
    title: str
    text: str
    created_at: str

    class Config:
        orm_mode = True
