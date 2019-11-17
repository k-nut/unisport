from sqlalchemy.orm import joinedload, subqueryload, contains_eager

from .app import app
from .models import SportsClass, Course, Location
from flask import request, jsonify


@app.route("/")
def main():
    return jsonify(data=[sc.to_dict() for sc in SportsClass.query.join(SportsClass.courses).options(joinedload(SportsClass.courses)).all()])


@app.route("/names")
def names():
    return jsonify(data=[sc.name for sc in SportsClass.query.all()])


@app.route("/locations")
def locations():
    return jsonify(data=[location.to_dict() for location in Location.query.all()])


@app.route("/classes", methods=["GET"])
def search():
    query = SportsClass.query.join(SportsClass.courses)

    if "name" in request.args:
        name = request.args["name"]
        query = query.filter((SportsClass.description.contains(name))|(SportsClass.name.contains(name))) # TODO: should not be case sensitive

    if "location" in request.args:
        query = query.filter(SportsClass.courses.any(Course.place == request.args["location"]))

    if "days" in request.args:
        query = query.filter(Course.day.in_(request.args["days"].split(",")))

    if "bookable" in request.args and request.args["bookable"] in ["true", "waitingList"]:
        bookable_states = ["buchen", "nur über Büro", "Karte kaufen", "anmeldefrei", "buchen 🔒", "Basisangebot", "siehe Text", "Kursdaten", "ohne Anmeldung"]
        waiting_states = ["Warteliste", "Warteliste 🔒"]
        if request.args["bookable"] == "true":
            allowed_states = bookable_states
        elif request.args["bookable"] == "waitingList":
            allowed_states = bookable_states + waiting_states
        query = query.filter(Course.bookable.in_(allowed_states))

    sports_classes = query \
        .options(contains_eager(SportsClass.courses)) \
        .all()

    sports_classes = [sports_class.to_dict() for sports_class in sports_classes]

    return jsonify(data=sports_classes)

