import os

import flask_cors
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from backend.models import db


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.33
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
flask_cors.CORS(app)
import backend.routes
