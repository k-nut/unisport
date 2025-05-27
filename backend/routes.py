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
    query_params = {
        "name": f"%{request.args.get('name', '')}%",
        "location": request.args.get("location"),
        "location_url": request.args.get("location_url"),
        "days": request.args.get("days", "").split(",") if request.args.get("days") else None,
        "bookable_states": None
    }

    bookable_states = ["buchen", "nur über Büro", "Karte kaufen", "anmeldefrei", "buchen 🔒", "Basisangebot", "siehe Text", "Kursdaten", "ohne Anmeldung"]
    waiting_states = ["Warteliste", "Warteliste 🔒"]

    if request.args.get("bookable") == "true":
        query_params["bookable_states"] = bookable_states
    elif request.args.get('bookable') == "waitingList":
        query_params["bookable_states"] = waiting_states + waiting_states

    sql = """
    WITH class_data AS (
        SELECT 
            c.name,
            c.description,
            c.url,
            json_agg(
                json_build_object(
                    'name', co.name,
                    'day', co.day,
                    'place', co.place,
                    'price', co.price,
                    'time', co.time,
                    'timeframe', co.timeframe,
                    'bookable', co.bookable
                )
            ) as courses
        FROM class c
        JOIN course co ON c.url = co.sports_class_url
        WHERE (:name IS NULL OR LOWER(c.description) LIKE LOWER(:name) OR LOWER(c.name) LIKE LOWER(:name))
          AND (:location IS NULL OR co.place = :location)
          AND (:location_url IS NULL OR co.place_url = :location_url)
          AND (:days IS NULL OR co.day = ANY(:days))
          AND (:bookable_states IS NULL OR co.bookable = ANY(:bookable_states))
        GROUP BY c.name, c.description, c.url
    )
    SELECT json_agg(
            json_build_object(
                'name', name,
                'description', description,
                'url', url,
                'courses', courses
            )
    ) as result
    FROM class_data;
    """

    with db.engine.connect() as conn:
        result = conn.execute(text(sql), query_params).scalar() or []
        
        # Log the search
        search_metric = Search(
            timestamp=datetime.datetime.now(),
            query=request.args,
            result_count=len(result)
        )
        db.session.add(search_metric)
        db.session.commit()
        
        return jsonify(dict(data=result))

