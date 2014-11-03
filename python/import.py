from models import SportsClass, db
import json

db.create_all()

with open("/home/knut/unisport/alle.json") as infile:
    classes = json.loads(infile.read())
    for sports_class in classes:
        m = SportsClass(sports_class["name"], sports_class["description"], sports_class["url"])
        db.session.add(m)
    db.session.commit()
