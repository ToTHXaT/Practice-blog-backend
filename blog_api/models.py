from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "User"

    username = Column(String(64), primary_key=True, index=True)
    password = Column(String(64))

    posts = relationship("Record", back_populates="user")


class Record(Base):
    __tablename__ = "Record"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    body = Column(Text)
    pub_date = Column(DateTime, index=True)

    user_id = Column(String(64), ForeignKey('User.username'))
    user = relationship("User", back_populates="posts")