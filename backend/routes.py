from models import app, SportsClass, Course, db, path_to_db
from flask import request, jsonify
import os
import datetime


@app.route("/")
def main():
    return jsonify(data=[sc.to_dict() for sc in db.session.query(SportsClass).all()])

@app.route("/age")
def age():
    return str(datetime.datetime.fromtimestamp(os.path.getmtime(path_to_db)))

@app.route("/names")
def names():
    return jsonify(data=[sc.name for sc in db.session.query(SportsClass).all()])

@app.route("/classes", methods=["GET"])
def search():
    if "name" in request.args:
        name = request.args["name"]
        sports_classes = db.session.query(SportsClass)\
                                   .filter((SportsClass.description.contains(name))|(SportsClass.name.contains(name)))\
                                   .all()
    else:
        sports_classes = db.session.query(SportsClass).all()

    sports_classes = [sports_class.to_dict() for sports_class in sports_classes]
    if "days" in request.args:
        days = request.args["days"].split(",")
        for sports_class in sports_classes:
            sports_class["courses"] = [course for
                                       course in sports_class["courses"]
                                       if course["day"] in days]
        sports_classes = [sc for sc in sports_classes if len(sc["courses"]) > 0]

    if "bookable" in request.args:
        if request.args["bookable"] == "true":
            allowed_states = ["buchen", "nur über Büro", "Karte kaufen", "anmeldefrei"]
        elif request.args["bookable"] == "waitingList":
            allowed_states = ["Warteliste", "buchen"]

        for sports_class in sports_classes:
            sports_class["courses"] = [course for
                                       course in sports_class["courses"]
                                       if course["bookable"] in allowed_states]
        sports_classes = [sc for sc in sports_classes if len(sc["courses"]) > 0]

    return jsonify(data=sports_classes)


if __name__ == "__main__":
    app.debug = True
    app.run()
