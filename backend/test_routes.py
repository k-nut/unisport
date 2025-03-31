import unittest

from backend.test_factory import create_sports_class, create_course, create_location
from .app import create_app
from .models import Search, db


app = create_app(database_uri="sqlite://")
app.config.update({
    "TESTING": True,
})

class DBTest(unittest.TestCase):
    def setUp(self):
        with app.app_context():
             db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_search_route_with_no_results(self):
        rv = self.app.get("/classes")
        assert rv.json == {"data": []}

    def test_simple_search(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            sc2 = create_sports_class(db.session, name="Judo")
            create_course(db.session, sports_class_url=sc.url)
            create_course(db.session, sports_class_url=sc.url)
            create_course(db.session, sports_class_url=sc2.url)
            db.session.commit()
        response = self.app.get("/classes?name=kicker")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 2

    def test_search_bookable(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            create_course(db.session, sports_class_url=sc.url, bookable="Warteliste")
            db.session.commit()
        response = self.app.get("/classes?name=kicker&bookable=true")
        classes = response.json["data"]
        assert len(classes) == 0

    def test_search_waiting_list(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            create_course(db.session, sports_class_url=sc.url, bookable="Warteliste")
            db.session.commit()
        response = self.app.get("/classes?name=kicker&bookable=waitingList")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 1

    def test_search_with_day_filter(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            create_course(db.session, sports_class_url=sc.url, day="Mo")
            create_course(db.session, sports_class_url=sc.url, day="Mi")
            db.session.commit()
        response = self.app.get("/classes?name=kicker&days=Mo,Di")
        classes = response.json['data']
        assert len(classes) == 1
        assert len(classes[0]["courses"]) == 1

    def test_search_with_location(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            sc2 = create_sports_class(db.session, name="Judo")
            matching_location = create_location(db.session, name='Kicker-Arena')
            other_location = create_location(db.session, name='Judohalle')
            create_course(db.session, sports_class_url=sc.url, place=matching_location.name)
            create_course(db.session, sports_class_url=sc2.url, place=other_location.name)
            db.session.commit()
        response = self.app.get("/classes?location=Kicker-Arena")
        classes = response.json['data']
        assert len(classes) == 1

    def test_search_with_location_url(self):
        with app.app_context():
            sc = create_sports_class(db.session, name="Kicker")
            sc2 = create_sports_class(db.session, name="Judo")
            matching_location = create_location(db.session, name='Kicker-Arena', url='https://example.org/kicker')
            other_location = create_location(db.session, name='Judohalle', url='https://example.org/judo-halle')
            create_course(db.session, sports_class_url=sc.url, place=matching_location.name, place_url=matching_location.url)
            create_course(db.session, sports_class_url=sc2.url, place=other_location.name, place_url=other_location.url)
            db.session.commit()
        response = self.app.get("/classes?location_url=https://example.org/kicker")
        classes = response.json['data']
        assert len(classes) == 1

    def test_names(self):
        with app.app_context():
            create_sports_class(db.session, name="Kicker")
            create_sports_class(db.session, name="Judo")
            db.session.commit()
        rv = self.app.get("/names")
        assert rv.json == {"data": ["Judo", "Kicker"]}

    def test_names_with_none(self):
        with app.app_context():
            create_sports_class(db.session, name="Kicker")
            create_sports_class(db.session, name=None)
            db.session.commit()
        rv = self.app.get("/names")
        assert rv.json == {"data": [None, "Kicker"]}

    def test_names_without_items(self):
        rv = self.app.get("/names")
        assert rv.json == {"data": []}

    def test_search_records_search(self):
        with app.app_context():
            assert db.session.query(Search).count() == 0
            kicker = create_sports_class(db.session, name="Kicker")
            create_sports_class(db.session, name="Judo")
            create_course(db.session, sports_class_url=kicker.url)
            db.session.commit()
        self.app.get("/classes?name=Kicker")
        with app.app_context():
            assert db.session.query(Search).count() == 1
            [search] = db.session.query(Search).all()
            assert search.result_count == 1
            assert search.query == {"name": "Kicker"}

    def test_search_records_search_with_no_results(self):
        with app.app_context():
            assert db.session.query(Search).count() == 0
            kicker = create_sports_class(db.session, name="Kicker")
            create_course(db.session, sports_class_url=kicker.url)
            db.session.commit()
        self.app.get("/classes?name=Tennis")
        with app.app_context():
            [search] = db.session.query(Search).all()
            assert search.result_count == 0
            assert search.query == {"name": "Tennis"}
