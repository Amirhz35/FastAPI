from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from typing import Annotated
from fastapi import Depends


URL_DATABASE = "postgresql://postgres:1234@localhost:5432/fastapi"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

