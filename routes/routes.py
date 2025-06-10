from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import RedirectResponse
from typing import Annotated

from schemas.schemas import *
from models import models
from sqlalchemy.orm import Session
from database import *

from services.url_logics import *

router = APIRouter()


@router.post('/post-urls')
async def post_urls(create_instance:URL_Create, db:db_dependency):
    try:
        request_url = create_instance.request_url
        shorturl = url_logic(request_url)
        URL_Read.short_url = shorturl
        URL_Read.original_url = request_url
        db_urls = models.URL(original_url=URL_Read.original_url,
                             short_url=URL_Read.short_url)
        db.add(db_urls)
        db.commit()
        db.refresh(db_urls)
        result = db.query(models.URL).filter(models.URL.original_url==request_url).first()
        url_with_domain = f"http://127.0.0.1:8000/{result.short_url}"
        return {
            "original_url": result.original_url,
            "short_url": url_with_domain
        }
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")

@router.get('/get-urls')
async def get_urls(db:db_dependency,original_url:str):
    try:
        result = db.query(models.URL).filter(models.URL.original_url==original_url).first()
        url_with_domain = f"http://127.0.0.1:8000/{result.short_url}"
        return {
            "original_url": result.original_url,
            "short_url": url_with_domain
        }
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")
    

@router.get('/{short_url}')
async def redirect_url(db:db_dependency,short_url:str):
    try:
        result = db.query(models.URL).filter(models.URL.short_url==short_url).first()
        return RedirectResponse(result.original_url)
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")

