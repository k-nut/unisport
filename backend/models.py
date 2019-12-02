from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, Float, ForeignKey

db = SQLAlchemy()


class SportsClass(db.Model):
    __tablename__ = "class"
    id = db.Column(db.Integer, primary_key=True)
    last_run = db.Column(db.DateTime)
    name = db.Column(db.String(200), index=True)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    courses = db.relationship("Course", backref="class")

    def __repr__(self):
        return "<SportsClass %s>" % self.name

    def to_dict(self):
        return {"name" : self.name,
                "description": self.description,
                "url": self.url,
                "courses": [course.to_dict() for course in self.courses]
               }


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    sports_class_url = Column(String, ForeignKey("class.url"))
    name = db.Column(db.String)
    day = db.Column(db.String)
    place = db.Column(db.String)
    place_url = Column(String)
    price = db.Column(db.String)
    time = db.Column(db.String)
    bookable = db.Column(db.String)
    timeframe = db.Column(db.String)

    def to_dict(self):
        return {"name": self.name,
                "day": self.day,
                "place": self.place,
                "price": self.price,
                "time": self.time,
                "timeframe": self.timeframe,
                "bookable": self.bookable
               }


class Location(db.Model):
    __tablename__ = "location"
    url = Column(String, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    def to_dict(self):
        return {"name": self.name,
                "lat": self.lat,
                "lon": self.lon,
                "url": self.url
                }
