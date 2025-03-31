from datetime import datetime
from backend.models import SportsClass, Course, Location

_counter = 0

def _get_unique_url():
    global _counter
    _counter += 1
    return f"http://example.com/{_counter}"

def create_sports_class(session, **kwargs):
    defaults = {
        "name": "Test Sports Class",
        "description": "Test description",
        "url": _get_unique_url(),
    }
    defaults.update(kwargs)
    sports_class = SportsClass(**defaults)
    session.add(sports_class)
    return sports_class

def create_course(session, **kwargs):
    defaults = {
        "sports_class_url": _get_unique_url(),
        "name": "Test Course",
        "day": "Mo",
        "place": "Test Place",
        "price": "10 / 20 / 30 / 40 Euro",
        "time": "12:00",
        "bookable": "true",
        "place_url": _get_unique_url()
    }
    defaults.update(kwargs)
    course = Course(**defaults)
    session.add(course)
    return course

def create_location(session, **kwargs):
    defaults = {
        "name": "Test Location",
        "lat": 52.10,
        "lon": 13.5,
        "url": _get_unique_url()
    }
    defaults.update(kwargs)
    location = Location(**defaults)
    session.add(location)
    return location
