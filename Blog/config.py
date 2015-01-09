# configuration settings file
import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog-dev.db"
    DEBUG = True
    # get application secret key from the environment
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
