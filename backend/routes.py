from prometheus_client import generate_latest, Gauge, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
from sqlalchemy.orm import joinedload, subqueryload, contains_eager

from .app import app
from .models import SportsClass, Course, Location, db
from flask import request, jsonify

# Create metrics for prometheus reporting
class_metric = Gauge('class_count', 'Class count', ['domain'])
location_metric = Gauge('location_count', 'Location count', ['domain'])
course_metric = Gauge('course_count', 'Course count', ['domain'])

# We do not want to expose any of the metrics that the prometheus_client
# exposes by default so we unregister them here.
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])


@app.route("/names")
def names():
    return jsonify(data=[sc[0] for sc in SportsClass.query.with_entities(SportsClass.name).all()])


@app.route("/locations")
def locations():
    return jsonify(data=[location.to_dict() for location in Location.query.all()])


@app.route("/metrics")
def stats():
    classes = db.engine.execute("""
    SELECT array_to_string(regexp_matches(url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
        from class
        group by domain
    """).all()
    for row in classes:
        class_metric.labels(domain=row[0]).set(row[1])

    locations = db.engine.execute("""
         SELECT array_to_string(regexp_matches(url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
         from location
         group by domain;
    """).all()
    for row in locations:
        location_metric.labels(domain=row[0]).set(row[1])

    courses = db.engine.execute("""
         SELECT array_to_string(regexp_matches(sports_class_url, 'https://([\w\-.]+)/'), ';') as domain, count(*) as count
         from course
         group by domain;
    """).all()
    for row in courses:
        course_metric.labels(domain=row[0]).set(row[1])

    return generate_latest()


@app.route("/classes", methods=["GET"])
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

    return jsonify(data=sports_classes)

