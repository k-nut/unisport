import datetime

from sqlalchemy import text
from sqlalchemy.orm import contains_eager

from .models import SportsClass, Course, Location, db, Search
from flask import request, jsonify, Blueprint

api = Blueprint('api', __name__)


@api.route("/names")
def names():
    return jsonify(data=[sc[0] for sc in SportsClass.query.with_entities(SportsClass.name).all()])


@api.route("/locations")
def locations():
    return jsonify(data=[location.to_dict() for location in Location.query.all()])


@api.route("/metrics")
def stats():
    with db.engine.connect() as conn:
        classes = conn.execute(text(r"""
        SELECT array_to_string(regexp_matches(url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
            from class
            group by domain
        """))
        class_metrics = [f'class_count{{domain="{row[0]}"}} {row[1]}' for row in classes]

        locations = conn.execute(text(r"""
             SELECT array_to_string(regexp_matches(url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
             from location
             group by domain;
        """))
        location_metrics = [f'location_count{{domain="{row[0]}"}} {row[1]}' for row in locations]

        courses = conn.execute(text(r"""
             SELECT array_to_string(regexp_matches(sports_class_url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
             from course
             group by domain;
        """))
        course_metrics = [f'course_count{{domain="{row[0]}"}} {row[1]}' for row in courses]

    return '\n'.join(class_metrics + location_metrics + course_metrics)


@api.route("/classes", methods=["GET"])
def search():
    query = SportsClass.query.join(SportsClass.courses)

    if "name" in request.args:
        name = "%{}%".format(request.args["name"])
        query = query.filter((SportsClass.description.ilike(name))|(SportsClass.name.ilike(name)))

    if "location" in request.args:
        query = query.filter(SportsClass.courses.any(Course.place == request.args["location"]))

    if "location_url" in request.args:
        query = query.filter(SportsClass.courses.any(Course.place_url == request.args["location_url"]))

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

    search_metric = Search(timestamp=datetime.datetime.now(),
                           query=request.args,
                           result_count=len(sports_classes))
    db.session.add(search_metric)
    db.session.commit()

    return jsonify(data=sports_classes)

