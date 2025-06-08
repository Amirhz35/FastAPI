from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated

from schemas.schemas import URL_schema
from models import models
from sqlalchemy.orm import Session
from database import *



router = APIRouter()
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session,Depends(get_db)]
'''

@router.post('/post-urls')
async def post_urls(url_instance:URL_schema,db:db_dependency):
    try:
        db_urls = models.URL(original_url=url_instance.original_url,
                              short_url=url_instance.short_url)
        db.add(db_urls)
        db.commit()
        db.refresh(db_urls)
        return {"every thing is ok",status.HTTP_200_OK}
    except HTTPException:
        return {"error":"pls try agian",status:status.HTTP_400_BAD_REQUEST}

@router.get('/get-urls')
async def get_urls(db:db_dependency):
    result = db.query(models.URL).all()
    return result