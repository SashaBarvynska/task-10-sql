from src.database.repositories.courses import CourseRepository
from src.database.models import CourseModel

data = {"student_id": 2, "course_id": [1]}


def test_get_all_courses(app, session):
    repo = CourseRepository(session)
    result = repo.get_all_courses()
    assert len(result) == 2


def test_create_course(app, session):
    repo = CourseRepository(session)
    result = repo.create_course("Nails")
    expected_data = (
        session.query(CourseModel).filter(CourseModel.name == result.name).first()
    )
    assert result == expected_data


def test_get_course_by_id(app, session):
    repo = CourseRepository(session)
    result = repo.get_course_by_id(2)
    expected_data = (
        session.query(CourseModel).filter(CourseModel.id == result.id).first()
    )
    assert result == expected_data


def test_delete_course_by_id(app, session):
    repo = CourseRepository(session)
    result = repo.delete_course_by_id(2)
    expected_data = session.query(CourseModel).filter(CourseModel.id == 2).first()
    assert result is expected_data
