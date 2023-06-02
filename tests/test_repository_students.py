from src.database.repositories.students import StudentRepository
from src.database.connection import db
from src.database.models import StudentModel, StudentCourseModel, CourseModel


data = {"first_name": "Susana", "last_name": "Bekirova"}


def valid_format_of_data(data):
    return [
        {"id": i.id, "first_name": i.first_name, "last_name": i.last_name} for i in data
    ]


def test_create_student(app):
    repo = StudentRepository(db.session)
    test_input = repo.create_student(data)
    expected_data = (
        db.session.query(StudentModel.id).filter(StudentModel.id == 1).first()
    )
    db.session.close()
    assert test_input.id == expected_data.id


def test_get_student_by_id(app):
    repo = StudentRepository(db.session)
    result = repo.get_student_by_id(2)
    db.session.close()
    assert result.id == 2


def test_delete_student_by_id(app):
    repo = StudentRepository(db.session)
    repo.delete_student_by_id(2)
    expected_data = (
        db.session.query(StudentModel.id).filter(StudentModel.id == 2).first()
    )
    db.session.close()
    assert expected_data is None


def test_get_students_related_to_course(app):
    repo = StudentRepository(db.session)
    test_input = repo.get_students_related_to_course("Biology")
    expected_data = (
        db.session.query(StudentModel)
        .join(StudentCourseModel)
        .join(CourseModel)
        .filter(StudentCourseModel.course_id == 1)
        .first()
    )
    db.session.close()
    assert test_input[0].id == expected_data.id


def test_get_all_students(app):
    expected_data = db.session.query(StudentModel).all()
    repo = StudentRepository(db.session)
    test_input = repo.get_all_students()
    db.session.close()
    assert valid_format_of_data(test_input) == valid_format_of_data(expected_data)
