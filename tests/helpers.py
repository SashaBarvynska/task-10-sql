from sqlalchemy.orm import Session
from src import StudentCourseModel, StudentModel, CourseModel, GroupModel


def add_data_to_db(session: Session) -> None:
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
    session.commit()


def delete_data_from_db(session: Session) -> None:
    session.query(StudentCourseModel).delete()
    session.query(CourseModel).delete()
    session.query(StudentModel).delete()
    session.query(GroupModel).delete()
    session.commit()
