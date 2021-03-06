# Application management file

import os
from flask.ext.script import Manager

from Blog import app
from Blog.models import Post, User
from Blog.database import session
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask.ext.migrate import Migrate, MigrateCommand # used to manage changes to the database schema
from Blog.database import Base

# create a class to hold the metadata object
class DB(object):

    def __init__(self, metadata):
        self.metadata = metadata



manager = Manager(app)

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# add some sample posts to the database
@manager.command
def seed():
    content = """ Lorem ipsum dolor sit amet, consectetur adipisicing elit,
                  sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
                  ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
                  in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
                  sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit
                  anim id est laborum.

             """
    for i in range(25):
        post = Post(
            title = "Test post #{}".format(i),
            content = content
        )
        session.add(post)

    # commit to database
    session.commit()

@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")

    if session.query(User).filter_by(email=email).first():
        print "User with that email already exists"
        return

    password = ""
    password_2 = ""

    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")

        user = User(name=name, email=email, password=generate_password_hash(password))
        session.add(user)
        session.commit()


if __name__ == '__main__':
    manager.run()

