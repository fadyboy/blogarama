# database models - tables and relationships

from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from flask.ext.login import UserMixin # Lets the User object inherit default login methods

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, Sequence("song_id_sequence"), primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey('users.id'))

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, Sequence("song_id_sequence"), primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

    # add relationship to posts
    posts = relationship("Post", backref="author")

    # add methods for User to use with Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<User - {}>".format(self.name)

# create database tables
Base.metadata.create_all(engine)

