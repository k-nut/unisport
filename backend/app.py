import os

import flask_cors
from flask import Flask

from backend.models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
flask_cors.CORS(app)
import backend.routes
