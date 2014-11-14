#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask
import flask_cors
from flask.ext.sqlalchemy import SQLAlchemy

import random

import os
import datetime

path_to_db = "/home/knut/unisport/everything.db"
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + path_to_db
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
    timeframe = db.Column(db.String)
    bookable = db.Column(db.String)

    def __init__(self, name, day, place, price, time, timeframe, bookable):
        self.name = name
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
                "timeframe": self.timeframe,
                "bookable": self.bookable
               }

