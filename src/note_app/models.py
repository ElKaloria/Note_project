from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean, ForeignKey

from src.auth.models import user

metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("text", String),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.utcnow()),
    Column("user", ForeignKey(user.c.id), nullable=False),
)
