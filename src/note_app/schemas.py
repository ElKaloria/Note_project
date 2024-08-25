from pydantic import BaseModel
from datetime import datetime


class NoteSchema(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


class CreateNote(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True
