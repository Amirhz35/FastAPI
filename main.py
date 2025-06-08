from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import Annotated
import models.models as models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from schemas.schemas import *
from routes.routes import router

app = FastAPI()
app.include_router(router)
models.Base.metadata.create_all(bind=engine)


