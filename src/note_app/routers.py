from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
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
    """
        Get all notes.

        Args:
            session (AsyncSession): The database session.
            page (int): The page number.
            limit (int): The number of notes per page.

        Returns:
            List[NoteSchema]: The list of notes.
    """

    offset = (page - 1) * limit
    query = select(notes).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.all()


@router.post("/create_note", response_model=CreateNote)
async def create_note(note: CreateNote = Depends(valid_text_and_title),
                      session: AsyncSession = Depends(get_async_session)):
    """
        Create a new note.

        Args:
            note (CreateNote): The note to create.
            session (AsyncSession): The database session.

        Returns:
            CreateNote: The created note.
    """

    stmt = insert(notes).values(**note)
    await session.execute(stmt)
    await session.commit()
    return note


@router.get("/{note_by_id}",
            response_model=NoteSchema)
async def get_note_by_id(note_by_id: NoteSchema | dict[str, str] = Depends(valid_post_id)):
    """
        Get a note by ID.

        Args:
            note_by_id NoteSchema | dict[str, str]: The note ID.

        Returns:
            NoteSchema | dict[str, str]: The note or error message.
    """

    return note_by_id

