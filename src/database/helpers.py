import random

from sqlalchemy.orm import Session as Session_type

from src.cli.logging_config import logging
from src.database.connection import db, get_session
from src.database.models import (
    CourseModel,
    GroupModel,
    StudentCourseModel,
    StudentModel,
)
from src.app import create_app
from .factories import CreateTestCourse, CreateTestStudent, GroupFactory
from config import Config

app = create_app(Config)


def create_tables() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()
        logging.info("created table in database.")


def assign_students_to_groups(session: Session_type) -> None:
    students_count = session.query(StudentModel).count()
    groups_count = session.query(GroupModel).count()
    students_in_groups = []
    for group_id in range(1, groups_count + 1):
        students_in_current_group = random.randint(10, 31)
        if (sum(students_in_groups) + students_in_current_group) <= students_count:
            student_ids = (
                session.query(StudentModel.id)
                .filter(StudentModel.group_id.is_(None))  # noqa: E711
                .limit(students_in_current_group)
            )

            session.query(StudentModel).filter(StudentModel.id.in_(student_ids)).update(
                {StudentModel.group_id: group_id}
            )

            students_in_groups.append(students_in_current_group)
    logging.info('Randomly assigned students to groups in table"s students')


def assign_random_courses(session: Session_type) -> None:
    list_ids = []
    students = session.query(StudentModel)
    courses = session.query(CourseModel).all()
    for student in students:
        num_courses = random.randint(1, 3)
        amount_course = random.sample(courses, num_courses)
        for course in amount_course:
            obj = StudentCourseModel(student_id=student.id, course_id=course.id)
            list_ids.append(obj)
    session.add_all(list_ids)
    logging.info(
        'Randomly assigned from 1 to 3 courses for each student in table"s student_course.'
    )


def insert_data() -> None:
    with app.app_context():
        with get_session() as session:
            groups = GroupFactory.create_batch(10)
            logging.info("Randomly created 10 groups in database")
            courses = CreateTestCourse.create_batch(10)
            logging.info("Randomly created 10 courses in database")
            students = CreateTestStudent.create_batch(200)
            logging.info("Randomly created 200 students in database")
            session.bulk_save_objects(groups)
            session.bulk_save_objects(courses)
            session.bulk_save_objects(students)
            assign_students_to_groups(session)
            assign_random_courses(session)
        logging.info("data added in database.")
