import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from dotenv import load_dotenv

load_dotenv()

db_url = "postgresql://{}:{}@{}:{}/{}".format(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME") )
engine = create_engine(db_url ,
                       pool_size=5,max_overflow=10,pool_timeout=30,pool_recycle=3600,pool_pre_ping=True)

class DBModel(DeclarativeBase):
    pass

def get_db():
    with Session(engine) as session:
        yield session
