from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.note_app.models import notes
from src.database import get_async_session
from src.note_app.schemas import NoteSchema, CreateNote

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.get("/", response_model=list[NoteSchema])
async def get_all_notes(session: AsyncSession = Depends(get_async_session),
                        page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    query = select(notes).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.all()


@router.post("/create_note", response_model=CreateNote)
async def create_note(note: CreateNote,
                      session: AsyncSession = Depends(get_async_session)):
    stmt = insert(notes).values(**note.dict())
    await session.execute(stmt)
    await session.commit()
    return note
