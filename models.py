#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import random

import os
import datetime

path_to_db = "/home/knut/unisport/everything.db"
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + path_to_db
db = SQLAlchemy(app)


class SportsClass(db.Model):
    ''' The represenation of a sportsclass in the database '''
    class_id = db.Column(db.Integer, primary_key=True)
    last_run = db.Column(db.DateTime)
    name = db.Column(db.String(200), index=True)
    description = db.Column(db.String)

    def __init__(self, name, description):
        self.class_id = random.randint(0, 1000000)
        self.name = name
        self.description = description

    def __repr__(self):
        return "<SportsClass %s>" % self.name

    def to_json(self):
        return {"name" : self.name,
                "description": self.description
               }
