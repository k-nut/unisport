from backend.app import app
from backend.models import db


with app.app_context():
    db.create_all()