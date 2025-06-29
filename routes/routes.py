from fastapi import APIRouter,Depends,HTTPException,status,Body
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas import *
from models import models
from sqlalchemy.orm import Session
from database import *
from datetime import datetime, timezone
from services.url_logics import *
from services.utils import *
from services.deps import *

router = APIRouter()


@router.post('/post-urls')
async def post_urls(create_instance:URL_Create, db:db_dependency,current_user: models.UserModel = Depends(get_current_user)):
    try:
        request_url = create_instance.request_url
        shorturl = url_logic(request_url)
        URL_Read.short_url = shorturl
        URL_Read.original_url = request_url
        db_urls = models.URL(original_url=URL_Read.original_url,
                             short_url=URL_Read.short_url,
                             user_id=current_user.id)
        db.add(db_urls)
        db.commit()
        db.refresh(db_urls)
        result = db.query(models.URL).filter(models.URL.original_url==request_url).first()
        url_with_domain = f"http://127.0.0.1:8000/{result.short_url}"
        return {
            "user_id": result.user_id,
            "original_url": result.original_url,
            "short_url": url_with_domain,
            "count": result.count,
            "is_active": result.is_active,
            "expire_time": result.expire_time
        }
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")
    


@router.get('/get-short-url')
async def get_short_url(db:db_dependency,original_url:str,current_user: User_login = Depends(get_current_user)):
    try:
        result = db.query(models.URL).filter(models.URL.original_url==original_url).first()
        url_with_domain = f"http://127.0.0.1:8000/{result.short_url}"
        return {
            "user_id": result.user_id,
            "original_url": result.original_url,
            "short_url": url_with_domain,
            "count": result.count,
            "is_active": result.is_active,
            "expire_time": result.expire_time
        }
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")
    


@router.get('/get-urls')
async def get_urls(db:db_dependency,current_user:User_login=Depends(get_current_user)):
    try:
        result = db.query(models.URL).filter(models.URL.user_id==current_user.id).all()
        return result
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")



@router.get('/s/{short_url}')
async def redirect_url(db:db_dependency,short_url:str):
    try:
        result = db.query(models.URL).filter(models.URL.short_url==short_url).first()
        time_now = datetime.now(timezone.utc)
        expire_time = result.expire_time
        if expire_time is not None:
            if expire_time < time_now:
                result.is_active = False
                db.commit()
                db.refresh(result)
                return {"error":"time has been expired"}
        result.count += 1
        db.commit()
        db.refresh(result)
        return RedirectResponse(result.original_url)
    except HTTPException:
        raise HTTPException(status_code=400,detail="something went wrong")




@router.post('/register')
async def register_user(db:db_dependency,user_instance:User_register):
    if db.query(models.UserModel).filter(models.UserModel.username==user_instance.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exist")
    db_user = models.UserModel(username=user_instance.username,
                                password=get_hashed_password(user_instance.password),
                                email=user_instance.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {f"user {db_user.username} created successfully"}




@router.post('/login')
async def login(db:db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    query = db.query(models.UserModel).filter(models.UserModel.username==form_data.username).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid username/password")
    hashed_pass = query.password
    if not verify_password(form_data.password,hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid username/password")

    return{
        "access_token": create_access_token(query.username),
        "refresh_token": create_refresh_token(query.username),
    }




@router.post('/expire')
async def set_expire_time(db: db_dependency, original_url:str, time_instance: Expire_Time = Body(description="pls write the time u want ur short link been expired"), current_user: models.UserModel = Depends(get_current_user)):
    expire_time = time_instance.expire_time
    query = db.query(models.URL).filter(models.URL.user_id==current_user.id,models.URL.original_url==original_url).first()
    query.expire_time = expire_time
    db.commit()
    db.refresh(query)
    time_now = datetime.now(timezone.utc)
    expire_time = query.expire_time
    if expire_time is not None:
        if expire_time > time_now:
            query.is_active = True
            db.commit()
            db.refresh(query)
    return query
