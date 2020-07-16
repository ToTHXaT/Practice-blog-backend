from typing import Optional

from datetime import datetime
from pydantic import BaseModel

class BaseUser(BaseModel):
    username : str

class CreateUser(BaseUser):
    password : str

class ChangeUser(BaseUser):
    new_password : str

class DBUser(CreateUser):

    class Config:
        orm_mode = True


class BasePost(BaseModel):
    title : str
    body : str

class RespPost(BasePost):
    pub_date : datetime

class ChangePost(BaseModel):
    id : int
    new_title : Optional[str]
    new_body : Optional[str]


class DBPost(RespPost):
    id : int
    user_id : str

    class Config:
        orm_mode = True