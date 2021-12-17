import sqlalchemy
from config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import SQLALCHEMY_ECHO_DEBUG


class MonPersistenceOrm:
    """
    Author: Lukas Fojtik, created on: 10.12.2019
    Class for communication with Monitoring MySQL DB
    Purpose is just to create / close session object while using context manager for instantiation.
    SqlAlchemy ORM engine and Base are class variables so every time this class is being used, reference points to the very same objects.
    This is needed mainly for Declarative Base object to gather all ORM models to one base so it can be applied for "create_all" (tables) etc..
    """

    # echo=True => print literal representation of final sql query to stdout
    engine = sqlalchemy.create_engine(settings.DB_URL, echo=SQLALCHEMY_ECHO_DEBUG)
    Base = declarative_base()

    def __init__(self):
        self._Session = sessionmaker()
        self._Session.configure(bind=self.engine)

    def __enter__(self):
        self.session = self._Session()
        return self

    def __exit__(self, *args):
        self.session.close()

    # @classmethod
    # def create_all(cls):
    #    cls.Base.metadata.create_all(cls.engine)


