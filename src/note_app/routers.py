from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.note_app.dependencies import valid_post_id, valid_text_and_title
from src.note_app.models import notes
from src.database import get_async_session, User
from src.note_app.schemas import NoteSchema, CreateNote

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/", response_model=list[NoteSchema])
async def get_all_notes(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session),
                        page: int = 1, limit: int = 10):
    """
        Get all notes.

        :arg:
            user (User): The current user.
            session (AsyncSession): The database session.
            page (int): The page number.
            limit (int): The number of notes per page.

        :return:
            List[NoteSchema]: The list of notes.
    """

    offset = (page - 1) * limit
    query = select(notes).where(notes.c.user == user.id).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.all()


@router.post("/create_note", response_model=CreateNote)
async def create_note(user: User = Depends(current_user), note: CreateNote = Depends(valid_text_and_title),
                      session: AsyncSession = Depends(get_async_session)):
    """
        Create a new note.

        :arg:
            user (User): The current user.
            note (CreateNote): The note to create.
            session (AsyncSession): The database session.

        :return:
            CreateNote: The created note.
    """

    stmt = insert(notes).values(**note, user=user.id)
    await session.execute(stmt)
    await session.commit()
    return note


@router.get("/{note_by_id}",
            response_model=NoteSchema)
async def get_note_by_id(user: User = Depends(current_user),
                         note_by_id: NoteSchema | dict[str, str] = Depends(valid_post_id)):
    """
        Get a note by ID.

        :arg:
            user (User): The current user.
            note_by_id (NoteSchema | dict[str, str]): The note ID.

        :return:
            NoteSchema | dict[str, str]: The note or error message.
    """

    return note_by_id
