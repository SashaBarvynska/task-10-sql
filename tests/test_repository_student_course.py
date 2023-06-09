from src.database.repositories.student_course import StudentCourseRepository
from src.database.models import StudentCourseModel, StudentModel, CourseModel

data = {"student_id": 2, "course_id": [1]}


def test_get_an_existing_course_from_the_student(app, session):
    repo = StudentCourseRepository(session)
    result = repo.get_an_existing_course_from_the_student(2, 2)
    assert result[0].id == 2


def test_get_course_to_student_by_id(app, session):
    repo = StudentCourseRepository(session)
    repo.add_student_to_course(3, 2)
    expected_data = (
        session.query(StudentModel)
        .join(StudentCourseModel)
        .join(CourseModel)
        .filter(StudentCourseModel.course_id == 3)
        .first()
    )
    assert expected_data.id == 2


def test_delete_course_to_student_by_id(app, session):
    get_row_from_from_StudentCourse = session.query(StudentCourseModel).first()
    repo = StudentCourseRepository(session)
    result = repo.delete_course_to_student_by_id(get_row_from_from_StudentCourse)
    assert result is None


def test_add_student_to_course(app, session):
    repo = StudentCourseRepository(session)
    repo.add_student_to_course(3, 2)
    get_row_from_from_StudentCourse = (
        session.query(StudentCourseModel.course_id)
        .filter(StudentCourseModel.course_id == 2)
        .first()
    )
    assert get_row_from_from_StudentCourse.course_id == 2
