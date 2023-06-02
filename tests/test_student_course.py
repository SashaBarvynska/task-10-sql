from src.database.repositories.student_course import StudentCourseRepository
from src.database.connection import db
from src.database.models import StudentCourseModel, StudentModel, CourseModel

data = {"student_id": 2, "course_id": [1]}


def test_add_student_to_course(app):
    repo = StudentCourseRepository(db.session)
    repo.add_student_to_course({"student_id": 2, "course_id": [2]}, 2)
    get_row_from_from_StudentCourse = (
        db.session.query(StudentCourseModel.course_id)
        .filter(StudentCourseModel.course_id == 2)
        .first()
    )
    db.session.close()
    assert 2 == get_row_from_from_StudentCourse.course_id


def test_delete_course_to_student_by_id(app):
    get_row_from_from_StudentCourse = db.session.query(StudentCourseModel).first()
    repo = StudentCourseRepository(db.session)
    result = repo.delete_course_to_student_by_id(get_row_from_from_StudentCourse)
    db.session.close()
    assert result is None


def test_get_an_existing_course_from_the_student(app):
    repo = StudentCourseRepository(db.session)
    result = repo.get_an_existing_course_from_the_student(data)
    db.session.close()
    assert result[0].id == 1


def test_get_course_to_student_by_id(app):
    repo = StudentCourseRepository(db.session)
    repo.add_student_to_course(data, (2,))
    expected_data = (
        db.session.query(StudentModel)
        .join(StudentCourseModel)
        .join(CourseModel)
        .filter(StudentCourseModel.course_id == 2)
        .first()
    )
    db.session.close()
    assert expected_data.id == 2
