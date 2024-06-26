import logging
import os

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(filename="events.log", level=logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:///" + os.path.join(basedir, "movies.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

OMDB_URL = os.environ["OMDB_URL"]
OMDB_APIKEY = os.environ["OMDB_APIKEY"]
MAX_AUTHORIZED_NUMBER = os.environ["MAX_AUTHORIZED_NUMBER"]
ADMIN_APIKEY = os.environ["ADMIN_APIKEY"]

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
