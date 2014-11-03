from models import SportsClass, db
import json

db.create_all()

with open("./alle.json") as infile:
    classes = json.loads(infile.read())
    for sports_class in classes:
        print(sports_class["name"])
        print(sports_class["description"])
        m = SportsClass(sports_class["name"], sports_class["description"])
        db.session.add(m)
    db.session.commit()
