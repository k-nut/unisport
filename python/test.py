from models import app
import routes
import unittest
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        path_to_db = "/home/knut/unisport/everything.db"
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + path_to_db
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root_route(self):
        rv = self.app.get("/")
        classes = json.loads(rv.data.decode("utf-8"))
        assert(True)

    def test_simple_search(self):
        response = self.app.get("/s/kicker")
        classes = json.loads(response.data.decode("utf-8"))
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 2

    def test_search_bookable(self):
        response = self.app.get("/s/kicker?bookable=true")
        classes = json.loads(response.data.decode("utf-8"))
        assert len(classes) == 0

    def test_search_waiting_list(self):
        response = self.app.get("/s/kicker?bookable=waitingList")
        classes = json.loads(response.data.decode("utf-8"))
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 1

if __name__ == '__main__':
    unittest.main()
