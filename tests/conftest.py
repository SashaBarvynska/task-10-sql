import pytest
from src.app import create_app
import config
from src.database.models import (
    StudentModel,
    CourseModel,
    StudentCourseModel,
    GroupModel,
)
from src.database.connection import db
from sqlalchemy.orm import Session


@pytest.fixture()
def app():
    app = create_app(config.TestConfig)
    with app.app_context():
        db.create_all()
        session: Session = db.session
        group = GroupModel(id=1, name="AA")
        session.add(group)
        session.flush()
        student = StudentModel(id=2, first_name="John", last_name="Doe", group_id=1)
        course_1 = CourseModel(id=1, name="Biology")
        course_2 = CourseModel(id=2, name="Math")
        session.add(student)
        session.add(course_1)
        session.add(course_2)
        session.flush()
        student_course = StudentCourseModel(student_id=2, course_id=1)
        session.add(student_course)
        session.flush()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
