from models import app, SportsClass
from flask import send_from_directory, request
import json


@app.route("/")
def main():
    return json.dumps([sc.to_json() for sc in SportsClass.query.all()])

@app.route("/s/<query>", methods=["GET"])
def search(query):
    sports_classes = SportsClass.query.filter(SportsClass.description.contains(query))
    if "days" in request.args:
        sports_classes = sports_classes.filter(SportsClass.courses.any(day=request.args.get("days")))

    filtered_classes = [sports_class.to_json()
                        for sports_class
                        in sports_classes
                       ]
    return json.dumps(filtered_classes)

@app.route("/kro")
def b():
    return "bla"

if __name__ == "__main__":
    app.debug = True
    app.run()
