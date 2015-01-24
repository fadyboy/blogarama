# database models - tables and relationships

from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Text
from database import Base, engine
from flask.ext.login import UserMixin # Lets the User object inherit default login methods

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, Sequence("post_id_sequence"), primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.now())

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_sequence"), primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

# create database tables
Base.metadata.create_all(engine)

