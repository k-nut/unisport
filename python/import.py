from models import SportsClass, db, Course
import json

db.create_all()

with open("/home/knut/unisport/alle.json") as infile:
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
