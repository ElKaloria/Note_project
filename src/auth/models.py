from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean, MetaData

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("username", String, nullable=False, unique=True),
    Column("registered_at", TIMESTAMP(timezone=True), default=datetime.utcnow()),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("hashed_password", String, nullable=False),
)
