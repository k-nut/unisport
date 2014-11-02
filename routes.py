from models import app, SportsClass
import json


@app.route("/")
def main():
    return "This is the startpage"

@app.route("/s/<query>")
def search(query):
    filtered_classes = [ sports_class.to_json() for sports_class in SportsClass.query.filter(SportsClass.description.contains(query))]
    return json.dumps(filtered_classes)

@app.route("/kro")
def b():
    return "bla"

if __name__ == "__main__":
    app.debug = True
    app.run()
