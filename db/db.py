from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite:///example.db")

class DBModel(DeclarativeBase):
    pass


