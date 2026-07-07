from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from db import db

class User(db.DBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))
    fullname: Mapped[Optional[str]]  # Nullable column


db.DBModel.metadata.create_all(db.engine)

