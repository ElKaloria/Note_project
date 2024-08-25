from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from src.note_app.dependencies import valid_post_id, valid_text_and_title
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
async def create_note(note: CreateNote = Depends(valid_text_and_title),
                      session: AsyncSession = Depends(get_async_session)):
    stmt = insert(notes).values(**note)
    await session.execute(stmt)
    await session.commit()
    return note


# @router.get("/{note_by_id}")
# async def get_note_by_id(note_by_id: NoteSchema = Depends(valid_post_id)):
#     return note_by_id
#
#
# @router.put("/{note_by_id}", response_model=NoteSchema)
# async def update_note_by_id(update_data: CreateNote,
#                             note_by_id: NoteSchema = Depends(valid_post_id),
#                             session: AsyncSession = Depends(get_async_session)):
#     stmt = notes.update().where(notes.c.id == note_by_id.id).values(**update_data.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return update_data
