from datetime import datetime

from sqlalchemy.orm import Session
import sqlalchemy.exc as sql

from fastapi import HTTPException

import shemas as shema
import models as model


def add_user(db : Session, user : shema.CreateUser):
    try:
        _user = model.User(**user.dict())

        db.add(_user)
        db.commit()
    except sql.IntegrityError:
        raise HTTPException(409, "User with this username already exists")
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def add_post(db : Session, post : shema.BasePost, user : shema.BaseUser):
    try:
        _post = model.Record(**post.dict(), user_id = user.username, pub_date=datetime.now())

        db.add(_post)
        db.commit()

    except sql.IntegrityError:
        raise HTTPException(409, "Integrity Error")
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def get_posts(db : Session, offset : int, limit : int):
    try:
        return db.query(model.Record).order_by(model.Record.pub_date.desc()).offset(offset).limit(limit).all()
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def get_user_posts(db : Session, user : shema.BaseUser, offset : int, limit : int):
    try:
        return db.query(model.User).filter(model.User.username == user.username).first().posts
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def upd_user(db : Session, user : shema.ChangeUser):
    try:
        _user = db.query(model.User).filter(model.User.username == user.username).one()

        _user.password = user.new_password

        db.add(_user)
        db.commit()
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def upd_post(db : Session, post : shema.ChangePost):
    try:
        _post = db.query(model.Record).filter(model.Record.id == post.id).one()

        if post.new_title:
            _post.title = post.new_title
        if post.new_body:
            _post.body = post.new_body

        db.add(_post)
        db.commit()
    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)

def del_post(db : Session, post_id : int):
    try:
        _post = db.query(model.Record).filter(model.Record.id == post_id).one()

        db.delete(_post)
        db.commit()

    except sql.SQLAlchemyError:
        raise HTTPException(400)
    except Exception:
        raise HTTPException(500)
