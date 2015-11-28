#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask
import flask_cors
from flask.ext.sqlalchemy import SQLAlchemy

import random

import os
import datetime

path_to_db = os.path.join(os.path.dirname(__file__), '../data/everything.db')
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(path_to_db)
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
flask_cors.CORS(app)


class SportsClass(db.Model):
    ''' The represenation of a sportsclass in the database '''
    __tablename__ = "sportsclass"
    id = db.Column(db.Integer, primary_key=True)
    last_run = db.Column(db.DateTime)
    name = db.Column(db.String(200), index=True)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    courses = db.relationship("Course", backref="sportsclass")

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return "<SportsClass %s>" % self.name

    def to_dict(self):
        return {"name" : self.name,
                "description": self.description,
                "url": self.url,
                "courses": [course.to_dict() for course in self.courses]
               }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("sportsclass.id"))
    name = db.Column(db.String)
    day = db.Column(db.String)
    place = db.Column(db.String)
    price = db.Column(db.String)
    time = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    bookable = db.Column(db.String)

    def __init__(self, name, day, place, price, time, timeframe, bookable):
        self.name = name
        parts = timeframe.split("-")
        if len(parts) > 1:
            self.start_date = parts[0]
            self.end_date = parts[1]
        else:
            self.start_date = self.end_date = parts[0]
        self.day = day
        self.place = place
        self.price = price
        self.time = time
        self.timeframe = timeframe
        self.bookable = bookable


    def to_dict(self):
        return {"name": self.name,
                "day": self.day,
                "place": self.place,
                "price": self.price,
                "time": self.time,
                "startDate": self.start_date,
                "endDate": self.end_date,
                "bookable": self.bookable
               }

