from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from db import db

class User(db.DBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(35))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(String(), unique=True)


db.DBModel.metadata.create_all(db.engine)

