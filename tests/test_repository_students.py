from src.database.repositories.students import StudentRepository
from src.database.models import StudentModel, StudentCourseModel, CourseModel


test_student = {"first_name": "Susana", "last_name": "Bekirova"}


def test_create_student(app, session):
    repo = StudentRepository(session)
    test_input = repo.create_student(test_student)
    expected_data = session.query(StudentModel.id).filter(StudentModel.id == 1).first()
    assert test_input.id == expected_data.id


def test_patch_student(app, session):
    student = StudentRepository(session).get_student_by_id(2)
    repo = StudentRepository(session)
    data = {"first_name": "Sasha", "last_name": "Barvynska"}
    repo.patch_student(student, data)
    expected_data = session.query(StudentModel).filter(StudentModel.id == 2).first()
    assert expected_data.first_name == "Sasha"


def test_get_student_by_id(app, session):
    repo = StudentRepository(session)
    result = repo.get_student_by_id(2)
    assert result.id == 2


def test_delete_student_by_id(app, session):
    repo = StudentRepository(session)
    repo.delete_student_by_id(2)
    expected_data = session.query(StudentModel.id).filter(StudentModel.id == 2).first()
    assert expected_data is None


def test_get_students_related_to_course(app, session):
    repo = StudentRepository(session)
    test_input = repo.get_students_related_to_course(2)
    expected_data = (
        session.query(StudentCourseModel)
        .filter(StudentCourseModel.course_id == 2)
        .first()
    )
    assert test_input[0].id == expected_data.student_id


def test_get_all_students(app, session):
    expected_data = session.query(StudentModel).all()
    repo = StudentRepository(session)
    test_input = repo.get_all_students()
    assert test_input == expected_data


def test_get_students_by_group_id(app, session):
    expected_data = session.query(StudentModel).all()
    repo = StudentRepository(session)
    test_input = repo.get_students_by_group_id(2)
    assert test_input == expected_data
