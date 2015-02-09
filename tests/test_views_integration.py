# tests for integration

import os
import unittest
from urlparse import urlparse
from werkzeug.security import generate_password_hash

# set configuration path to use testing database
os.environ["CONFIG_PATH"] = "Blog.config.TestingConfig"

from Blog import app, models
from Blog.database import Base, session, engine

class TestViews(unittest.TestCase):

    def setUp(self):
        """
        Test setup
        """
        self.client = app.test_client() # test client

        # create tables in database
        Base.metadata.create_all(engine)

        # create sample user
        self.user = models.User(name="Alice", email="alice@test.com", password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """
        Test teardown
        """
        Base.metadata.drop_all(engine)

    def simulate_login(self):

        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id) # user id of post author
            http_session["_fresh"] = True # key that tells app that session is still active

    def login_and_post(self):
        self.simulate_login()
        self.client.post("/post/add", data={"title":"Test Title", "content":"Test Content"})

    def testAddPost(self):
        # login
        self.simulate_login()
        # add post to app
        response = self.client.post("/post/add", data={"title":"Test Title", "content": "Test Content"})

        self.assertEqual(response.status_code, 302)
        # check that user is returned to homepage after adding post
        self.assertEqual(urlparse(response.location).path, "/")

        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.content, "<p>Test Content</p>\n")
        self.assertEqual(post.author, self.user)

    def testEditPost(self):
        # login and add a post
        self.login_and_post()

        posts = session.query(models.Post).all()
        post = posts[0]
        # verify current post title
        self.assertEqual(post.title, "Test Title")
        # Edit post title and content
        post.title = "Test Title Edit"
        post.content = "This is new content"

        self.assertEqual(post.title, "Test Title Edit")
        self.assertEqual(post.content, "This is new content")
        self.assertEqual(len(posts), 1) # verify same post edited by confirming only 1 post in db

    def testDeletePost(self):
        # login and add a post
        self.login_and_post()
        # confirm post added
        posts = session.query(models.Post).all()
        post = posts[0]
        post_to_delete = session.query(models.Post).get(post.id)
        self.assertEqual(len(posts), 1)
        # delete post and confirm delete
        session.delete(post_to_delete)
        session.commit()
        # confirm post count after delete
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 0)


