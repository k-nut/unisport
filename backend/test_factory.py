import factory

from backend.models import SportsClass, Course, Location, db

class SportsClassFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SportsClass
        sqlalchemy_session = db.session   # the SQLAlchemy session object
        sqlalchemy_session_persistence = 'commit'

    # id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'SportsClass %d' % n)
    description = factory.Faker('text')
    url = factory.Faker('uri')


class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session = db.session   # the SQLAlchemy session object
        sqlalchemy_session_persistence = 'commit'
    sports_class_url = factory.Faker('uri')
    name = factory.Sequence(lambda n: u'Course %d' % n)
    # day = factory.Faker('random_element', ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So', 'tägl.'])
    day = 'Mo'
    place = 'The place'
    price = '10 / 20 / 30 / 40 Euro'
    time = '12:00'
    bookable = 'true'


class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = db.session   # the SQLAlchemy session object
        sqlalchemy_session_persistence = 'commit'
    name = factory.Faker('address')
    lat = '52.10'
    lon = '13.5'
    url = factory.Faker('uri')
