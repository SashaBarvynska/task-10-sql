from flask_restful import Resource

from flask import request
from http import HTTPStatus
from src.database.repositories import (
    StudentCourseRepository,
    StudentRepository,
    CourseRepository,
)
from src.database.connection import get_session
from flask import wrappers
from dataclasses import asdict
from src.api.dataclass import Student, Course


# delete a student from the course
class CourseStudentApi(Resource):
    def delete(self, course_id, student_id) -> wrappers.Response:
        with get_session() as session:
            student_course_repository = StudentCourseRepository(session)
            course = student_course_repository.get_course_to_student_by_id(
                course_id, student_id
            )
            if not course:
                return {
                    "error": f"Course by id {course_id} not found."
                }, HTTPStatus.NOT_FOUND
            else:
                student_course_repository.delete_course_to_student_by_id(course)
            return {
                "message": f"Course by id {course.course_id} has been deleted."
            }, HTTPStatus.OK


class CourseStudentListAPI(Resource):
    # get all students in the course
    def get(self, course_id) -> wrappers.Response:
        with get_session() as session:
            students = StudentRepository(session).get_students_related_to_course(
                course_id
            )
            dict_students = list(
                map(
                    lambda student: asdict(
                        Student(student.id, student.first_name, student.last_name)
                    ),
                    students,
                )
            )
            return dict_students, HTTPStatus.OK

    #  add a student to the course
    def post(self, course_id) -> wrappers.Response:
        with get_session() as session:
            data = request.get_json()
            student_id = data["student_id"]
            student_course_repository = StudentCourseRepository(session)
            course_id_exist = (
                student_course_repository.get_an_existing_course_from_the_student(
                    course_id, student_id
                )
            )
            if course_id_exist:
                return {
                    "error": f"This course by id  {[course_id[0] for course_id in course_id_exist][0]} already exists."
                }, HTTPStatus.NOT_FOUND
            else:
                student_course_repository.add_student_to_course(course_id, student_id)
                return {"message": "Course was added successfully."}, HTTPStatus.OK


class CoursesListApi(Resource):
    #  get all courses
    def get(self) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            courses = course_repository.get_all_courses()
            dict_courses = list(
                map(
                    lambda course: asdict(
                        Course(course.id, course.name, course.description)
                    ),
                    courses,
                )
            )
            return dict_courses, HTTPStatus.OK

    #  create a new course
    def post(self) -> wrappers.Response:
        with get_session() as session:
            data = request.get_json()
            name_course = data["name"]
            course_repository = CourseRepository(session)
            course_repository.create_course(name_course)
            return {"message": "Course was created successfully."}, HTTPStatus.OK


class CourseApi(Resource):
    # get course by id
    def get(self, course_id):
        with get_session() as session:
            course_repository = CourseRepository(session)
            course = course_repository.get_course_by_id(course_id)
            dict_course = asdict(Course(course.id, course.name, course.description))
            return dict_course, HTTPStatus.OK

    # delete course by id
    def delete(self, course_id: int) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            course = course_repository.get_course_by_id(course_id)
            if not course:
                return {
                    "error": f"Course by {course_id} not found."
                }, HTTPStatus.NOT_FOUND
            else:
                course_repository.delete_course_by_id(course_id)
                return {
                    "message": f"Course by {course_id} has been deleted."
                }, HTTPStatus.OK
