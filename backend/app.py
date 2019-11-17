import os

import flask_cors
from flask import Flask

from backend.models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db.init_app(app)
flask_cors.CORS(app)
import backend.routes