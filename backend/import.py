from models import SportsClass, db, Course
import json
import os


JSON_PATH = os.environ.get('UNISPORT_JSON_PATH')
DB_PATH = os.environ.get('UNISPORT_DB_PATH')

# delete the old database so that we can start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

db.create_all()

with open(os.path.join(JSON_PATH, "alle.json")) as infile:
    classes = json.loads(infile.read())
    for sports_class in classes:
        print(sports_class)
        m = SportsClass(sports_class["name"], sports_class["description"], sports_class["url"])
        if "dates" in sports_class:
            for course in sports_class["dates"]:
                c = Course(course["name"], course["day"], course["place"], course["price"], course["time"], course["timeframe"], course["bookable"])
                db.session.add(c)
                m.courses.append(c)

        db.session.add(m)
    db.session.commit()
