from models import app, SportsClass, Course, db
from flask import send_from_directory, request
import json


@app.route("/")
def main():
    return json.dumps([sc.to_dict() for sc in db.session.query(SportsClass).all()])

@app.route("/s/<query>", methods=["GET"])
def search(query):
    sports_classes = db.session.query(SportsClass)\
                               .filter((SportsClass.description.contains(query))|(SportsClass.name.contains(query)))\
                               .join(Course)
    sports_classes = [sports_class.to_dict() for sports_class in sports_classes]
    if "days" in request.args:
        sports_classes = sports_classes.filter(SportsClass.courses.any(day=request.args.get("days")))

    if "bookable" in request.args:
        if request.args["bookable"] == "true":
            allowed_states = ["buchen"]
        elif request.args["bookable"] == "waitingList":
            allowed_states = ["Warteliste", "buchen"]

        for sports_class in sports_classes:
            sports_class["courses"] = [course for
                                       course in sports_class["courses"]
                                       if course["bookable"] in allowed_states]
        sports_classes = [sc for sc in sports_classes if len(sc["courses"]) > 0]

    return json.dumps(sports_classes)


if __name__ == "__main__":
    app.debug = True
    app.run()
