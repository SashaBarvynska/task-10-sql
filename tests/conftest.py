import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import TestConfig
from main import app as flask_app
from src import StudentModel


@pytest.fixture(scope="module")
def app():
    flask_app.config.from_object(TestConfig)
    yield flask_app


@pytest.fixture(scope="module")
def client(app):
    yield app.test_client()


Base_test = declarative_base()


@pytest.fixture(scope='session')
def test_db(app):
    test_db = create_engine(TestConfig.TEST_DATABASE)
    Session = sessionmaker(bind=test_db)
    session = Session()
    session.query(StudentModel)
    Base_test.metadata.create_all(bind=test_db)
    yield test_db
    Base_test.metadata.drop_all(bind=test_db)
