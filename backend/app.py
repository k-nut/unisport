import os

import flask_cors
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.05
)

def create_app(database_uri=os.environ.get("DATABASE_URL")):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    flask_cors.CORS(app)

    from backend.models import db
    db.init_app(app)

    from backend.routes import api
    app.register_blueprint(api)

    return app