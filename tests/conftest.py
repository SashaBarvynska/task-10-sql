import pytest
import sys, os

sys.path.append(os.getcwd())
from tests.helpers import add_data_to_db, delete_data_from_db

from src.app import create_app
from config import TestConfig
from sqlalchemy.sql import text
from src.database.connection import db as _db
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope="function")
def session(app, db):
    session: Session = db.session
    session.execute(text("ALTER SEQUENCE students_id_seq RESTART;"))
    add_data_to_db(session)
    yield session
    delete_data_from_db(session)
    session.close()


@pytest.fixture()
def client(app):
    return app.test_client()
