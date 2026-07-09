from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped
from db import db

class User(db.DBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    fullname: Mapped[str] = mapped_column(String(35))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(String(18), unique=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


db.DBModel.metadata.create_all(db.engine)

