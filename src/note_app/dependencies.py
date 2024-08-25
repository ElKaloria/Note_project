from typing import Any, Tuple

import requests
from fastapi import Depends
from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.note_app.schemas import CreateNote
from src.note_app.models import notes
from src.database import get_async_session
from fastapi import Response


async def valid_post_id(post_id: int,
                        response: Response,
                        session: AsyncSession = Depends(get_async_session)) -> Row[tuple[Any]] | dict[str, str]:
    """
        Check if a post with the given ID exists in the database.

        Args:
            post_id (int): The ID of the post to check.
            response (Response): The response object to set the status code on if the post is not found.
            session (AsyncSession, optional): The database session to use. Defaults to the session returned by get_async_session.

        Returns:
           Row[tuple[Any]] | Dict[str, str]: The post data if it exists, or messeges if it doesn't.
    """

    query = select(notes).where(notes.c.id == post_id)
    post = await session.execute(query)
    result = post.first()
    if not result:
        response.status_code = 404
        return {"description": "Note not found"}

    return result


async def valid_text_and_title(note: CreateNote) -> dict[str, str]:
    """
        Check the spelling of the note's title and text using the Yandex Speller API.

        Args:
            note (CreateNote): The note to check.

        Returns:
            Dict[str, str]: The note data with corrected spelling.
    """

    spell_note_text = requests.get(f"https://speller.yandex.net/services/"
                                   f"spellservice.json/checkText?text={note.text}").json()
    spell_note_title = requests.get(f"https://speller.yandex.net/services/"
                                    f"spellservice.json/checkText?text={note.title}").json()
    note = note.dict()
    for text_item in spell_note_text:
        note["text"] = note["text"].replace(text_item["word"], text_item["s"][0])
    for title_item in spell_note_title:
        note["title"] = note["title"].replace(title_item["word"], title_item["s"][0])

    return note
