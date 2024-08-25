from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP

metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("text", String),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.utcnow()),
)
