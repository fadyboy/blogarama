# database models - tables and relationships

from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Text
from database import Base, engine

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, Sequence("post_id_sequence"), primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.now())

# create database tables
Base.metadata.create_all(engine)

