from models import app, SportsClass
from flask import send_from_directory
import json


@app.route("/")
def main():
    return json.dumps([sc.to_json() for sc in SportsClass.query.all()])

@app.route("/s/<query>")
def search(query):
    filtered_classes = [sports_class.to_json()
                        for sports_class
                        in SportsClass.query.filter(SportsClass.description.contains(query))
                                            .filter(SportsClass.courses.any(day="Mi"))
                       ]
    return json.dumps(filtered_classes)

@app.route("/kro")
def b():
    return "bla"

if __name__ == "__main__":
    app.debug = True
    app.run()
