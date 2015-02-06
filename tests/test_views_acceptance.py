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


    def testLoginCorrect(self):
        # self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice4@test.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
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

# use when not running with Nose
# if __name__ == "__main__":
#     unittest.main()




