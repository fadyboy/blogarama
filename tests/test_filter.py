# create unit test to test filter

import os
import unittest
import datetime

# configure app to use config from environment
os.environ["CONFIG_PATH"] = "Blog.config.TestingConfig"

import Blog
from Blog.filters import *

class FiltersTest(unittest.TestCase):

    def testDateFormat(self):
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    def testDateFormatNone(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)

# if __name__ == "__main__":
#     unittest.main