from typing import List

from fastapi import Depends, FastAPI, HTTPException, Body, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from db import SessionLocal
import crud

import shemas as shema
import models as model


api = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

SECRET_KEY = "c82588ed44c4844a214db35c6ad7b190db259a1043913b16"

manager = LoginManager(SECRET_KEY, "api/auth/token")

@manager.user_loader
def load_user(username: str):
    db = SessionLocal()
    user = db.query(model.User).filter(model.User.username == username).one()

    return {"username" : user.username, "password" : user.password}

@api.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@api.post("/signup", status_code=201)
async def singup_user(user : shema.CreateUser, db : Session = Depends(get_db)):
    crud.add_user(db, user)

@api.get("/posts", response_model=List[shema.DBPost], status_code=200)
async def get_posts(offset : int = 0, limit : int = 10,db: Session = Depends(get_db)):
    return crud.get_posts(db, offset, limit)

@api.post("/posts", status_code=201)
async def add_post(post : shema.BasePost,user = Depends(manager), db : Session = Depends(get_db)):
    crud.add_post(db, post, shema.BaseUser(username=user['username']))

@api.get("/user/posts")
async def get_user_posts(offset : int = 0, limit : int = 10, db : Session = Depends(get_db), user = Depends(manager)):
    return crud.get_user_posts(db, shema.BaseUser(username=user['username']), offset, limit)

@api.put("/user/update", status_code=200)
async def update_user(new_user : shema.ChangeUser, db : Session = Depends(get_db), user = Depends(manager)):
    crud.upd_user(db, new_user)

@api.put("/posts/update", status_code=200)
async def update_post(post : shema.ChangePost, db : Session = Depends(get_db), user = Depends(manager)):
    crud.upd_post(db, post)

@api.delete("/post/delete", status_code=200)
async def delete_post(post_id : int = Body(..., embed=True), db : Session = Depends(get_db), user = Depends(manager)):
    crud.del_post(db, post_id)
