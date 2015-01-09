# application file
import os
from flask import Flask


app = Flask(__name__)

# add configuration
config_path = os.environ.get("CONFIG_PATH", "Blog.config.DevelopmentConfig")
app.config.from_object(config_path)

import views, filters
