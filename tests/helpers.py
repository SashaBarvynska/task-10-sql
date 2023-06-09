from sqlalchemy.orm import Session
from src import StudentCourseModel, StudentModel, CourseModel, GroupModel


def add_data_to_db(session: Session) -> None:
    group_1 = GroupModel(id=2, name="AA")
    group_2 = GroupModel(id=3, name="BB")
    session.add(group_1)
    session.add(group_2)
    session.flush()
    student = StudentModel(id=2, first_name="John", last_name="Doe", group_id=2)
    course_1 = CourseModel(id=2, name="Biology")
    course_2 = CourseModel(id=3, name="Math")
    session.add(student)
    session.add(course_1)
    session.add(course_2)
    session.flush()
    student_course = StudentCourseModel(student_id=2, course_id=2)
    session.add(student_course)
    session.flush()
    session.commit()


def delete_data_from_db(session: Session) -> None:
    session.query(StudentCourseModel).delete()
    session.query(CourseModel).delete()
    session.query(StudentModel).delete()
    session.query(GroupModel).delete()
    session.commit()
