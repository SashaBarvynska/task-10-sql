import random

from sqlalchemy import text
from sqlalchemy.orm import Session as Session_type
from sqlalchemy.orm import sessionmaker

from logging_config import logging
from src.database.connection import Base, db
from src.database.fixture import (CreateTestCourse, CreateTestStudent,
                                  GroupFactory)
from src.database.models import (CourseModel, GroupModel, StudentCourseModel,
                                 StudentModel)

Session = sessionmaker(bind=db)


def create_tables() -> None:
    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all(bind=db)
    logging.info('created table in database.')


def assing_students_to_groups(session: Session_type) -> None:
    students_count = session.query(StudentModel).count()
    groups_count = session.query(GroupModel).count()
    students_in_groups = []
    for group_id in range(1, groups_count + 1):
        students_in_current_group = random.randint(10, 31)
        if (sum(students_in_groups) + students_in_current_group) <= students_count:
            student_ids = session.query(StudentModel.student_id).filter(
                StudentModel.group_id == None  # noqa: E711
                ).limit(
                    students_in_current_group
                    )

            session.query(StudentModel).filter(
                StudentModel.student_id.in_(student_ids)
                ).update(
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
            obj = StudentCourseModel(student_id=student.student_id, course_id=course.course_id)
            list_ids.append(obj)
    session.add_all(list_ids)
    logging.info('Randomly assigned from 1 to 3 courses for each student in table"s student_course.')


def insert_data_in_db() -> None:
    session = Session()

    groups = GroupFactory.create_batch(10)
    logging.info('Randomly created 10 groups in database')
    courses = CreateTestCourse.create_batch(10)
    logging.info('Randomly created 10 courses in database')
    students = CreateTestStudent.create_batch(200)
    logging.info('Randomly created 200 students in database')
    session.execute(text('ALTER SEQUENCE students_student_id_seq RESTART WITH 1;'))
    session.bulk_save_objects(groups)
    session.bulk_save_objects(courses)
    session.bulk_save_objects(students)
    assing_students_to_groups(session)
    assign_random_courses(session)
    session.commit()
    logging.info('data added in database.')
