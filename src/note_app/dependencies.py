from typing import Any

import requests
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.note_app.schemas import CreateNote
from src.note_app.models import notes
from src.database import get_async_session


async def valid_post_id(post_id: int,
                        session: AsyncSession = Depends(get_async_session)) -> dict[str, str] | Any:
    query = select(notes).where(notes.c.id == post_id)
    post = await session.execute(query)
    print(post)
    if not post:
        return {"error": "post not found"}

    return post.first()


async def valid_text_and_title(note: CreateNote):
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
