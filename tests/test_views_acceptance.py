# acceptance tests for blog application

import os
import unittest
import multiprocessing
# from urlparse import urlparse
import time
from werkzeug.security import generate_password_hash
from splinter import Browser

# set config path to map to test configuration settings
os.environ["CONFIG_PATH"] = "Blog.config.TestingConfig"

from Blog import app
from Blog import models
from Blog.database import session, Base, engine

class TestViews(unittest.TestCase):

    def setUp(self):
        # set browser driver to phantomjs
        self.browser = Browser("phantomjs")
        # self.browser = Browser()

        # create database tables
        Base.metadata.create_all(engine)

        # add sample user to db
        self.user = models.User(name="Alice", email="alice4@test.com", password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()


        # start a new process for Flask test server to run on
        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1) # pause for 1 sec for server to start


    def tearDown(self):
        # drop tables in db, kill process, and close browser
        self.process.terminate()
        Base.metadata.drop_all(engine)
        self.browser.quit()

    # create function to login
    def login(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice4@test.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()

    # create function to add post as action is repeated a few times
    def add_post(self):
        add_post_link = self.browser.find_link_by_text("Add Post")
        add_post_link.click()
        self.browser.fill("title", "This is a test title")
        self.browser.fill("content", "This is test content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()


    def testLoginCorrect(self):
        # self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice4@test.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        print "url", self.browser.url
        # self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")


    def testLoginIncorrect(self):
        # self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.visit("http://127.0.0.1:5000/login")
        # enter incorrect login details
        self.browser.fill("email", "james@test.com")
        self.browser.fill("password", "james")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        # user returned to login page
        # self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")

    def testAddPost(self):
        """
        Test to add post and view the post page
        """
        self.login()
        add_post_link = self.browser.find_link_by_text("Add Post")
        add_post_link.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/add")
        self.browser.fill("title", "Test Title")
        self.browser.fill("content", "Adding Content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        # verify user is redirected to the homepage and post is visible on page
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        # find link to post and open
        posted_link = self.browser.find_link_by_href("/post/1")
        posted_link.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1")

    def testEditPost(self):
        """
        Test to edit post
        """
        # login and add post
        self.login()
        self.add_post()
        # click the Edit button for the post
        edit_button = self.browser.find_by_css("button[name=edit]")
        edit_button.click()
        # confirm edit page for post is displayed
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1/edit")
        # edit the title and content
        self.browser.fill("title", "Edited Title")
        self.browser.fill("content", "Edited Content")
        submit = self.browser.find_by_css("button[type=submit]")
        submit.click()
        # verify edited title and content changes
        title_text = self.browser.is_text_present("Edited Title")
        content_text = self.browser.is_text_present("Edited Content")
        self.assertEqual(title_text, True)
        self.assertEqual(content_text, True)

    def testDeletePost(self):
        """
        Test to delete post
        """
        # login and add a post
        self.login()
        self.add_post()
        delete_button = self.browser.find_by_css("button[name=delete]")
        delete_button.click()
        # confirm delete page for post displayed
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1/delete")
        confirm_delete = self.browser.find_by_css("button[name=confirm]")
        confirm_delete.click()
        # verify post no longer present on homepage
        post_deleted = self.browser.is_text_not_present("This is a test title")
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.assertEqual(post_deleted, True)

    def testCancelDelete(self):
        """
        Test to cancel delete of post
        """
        self.login()
        self.add_post()
        delete_button = self.browser.find_by_css("button[name=delete]")
        delete_button.click()
        # confirm delete page for displayed and click Cancel button
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1/delete")
        cancel_delete = self.browser.find_by_css("button[name=cancel]")
        cancel_delete.click()
        # verify that post is still displayed on homepage
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        post_present = self.browser.is_text_present("This is a test title")
        self.assertEqual(post_present, True)





# use when not running with Nose
# if __name__ == "__main__":
#     unittest.main()




