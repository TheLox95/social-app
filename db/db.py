from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///example.db",
                       pool_size=5,max_overflow=10,pool_timeout=30,pool_recycle=3600,pool_pre_ping=True)

class DBModel(DeclarativeBase):
    pass

def get_db():
    with Session(engine) as session:
        yield session
