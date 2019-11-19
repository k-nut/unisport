import unittest

from backend.test_factory import SportsClassFactory, CourseFactory, LocationFactory
from .app import db, app


class DBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        with app.app_context():
            for table in reversed(db.metadata.sorted_tables):
                db.engine.execute(table.delete())
            db.session.commit()
            db.session.remove()

    def test_root_route_with_no_resulst(self):
        rv = self.app.get("/")
        assert rv.json == {"data": []}

    def test_simple_search(self):
        with app.app_context():
            sc = SportsClassFactory.create(name="Kicker")
            sc2 = SportsClassFactory.create(name="Judo")
            CourseFactory.create(sports_class_url=sc.url)
            CourseFactory.create(sports_class_url=sc.url)
            CourseFactory.create(sports_class_url=sc2.url)
        response = self.app.get("/classes?name=kicker")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 2

    def test_search_bookable(self):
        with app.app_context():
            sc = SportsClassFactory.create(name="Kicker")
            CourseFactory.create(sports_class_url=sc.url, bookable="Warteliste")
        response = self.app.get("/classes?name=kicker&bookable=true")
        classes = response.json["data"]
        assert len(classes) == 0

    def test_search_waiting_list(self):
        with app.app_context():
            sc = SportsClassFactory.create(name="Kicker")
            CourseFactory.create(sports_class_url=sc.url, bookable="Warteliste")
        response = self.app.get("/classes?name=kicker&bookable=waitingList")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 1

    def test_search_with_day_filter(self):
        with app.app_context():
            sc = SportsClassFactory.create(name="Kicker")
            CourseFactory.create(sports_class_url=sc.url, day="Mo")
            CourseFactory.create(sports_class_url=sc.url, day="Mi")
        response = self.app.get("/classes?name=kicker&days=Mo,Di")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 1

    def test_search_with_location(self):
        with app.app_context():
            sc = SportsClassFactory.create(name="Kicker")
            sc2 = SportsClassFactory.create(name="Judo")
            matching_location = LocationFactory.create(name='Kicker-Arena')
            other_location = LocationFactory.create(name='Judohalle')
            CourseFactory.create(sports_class_url=sc.url, place=matching_location.name)
            CourseFactory.create(sports_class_url=sc2.url, place=other_location.name)
        response = self.app.get("/classes?location=Kicker-Arena")
        classes = response.json['data']
        assert len(classes) == 1
