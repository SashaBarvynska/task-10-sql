from flask_restful import Resource

from http import HTTPStatus
from src.database.repositories import (
    StudentCourseRepository,
    StudentRepository,
    CourseRepository,
)
from src.database.connection import get_session
from flask import wrappers
from dataclasses import asdict
from src.api.dataclass import StudentDataclass, CourseDataclass
from src.swagger.courses import (
    StudentsIdSchema,
    CourseNotFoundSchema,
    CourseRequestSchema,
    CourseResponseSchema,
    DeleteCourseSchema,
    AddCourseRequestSchema,
    DeleteCourseStudentSchema,
    AddCourseStudentRequestSchema,
)
from src.api.students import StudentResponseSchema
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource


class CourseStudentApi(MethodResource, Resource):
    @doc(description="Delete course to student", tags=["Courses"])
    @marshal_with(DeleteCourseStudentSchema, code=200)
    @marshal_with(CourseNotFoundSchema, code=404)
    def delete(self, course_id, student_id) -> wrappers.Response:
        with get_session() as session:
            student_course_repository = StudentCourseRepository(session)
            course = student_course_repository.get_course_to_student_by_id(
                course_id, student_id
            )
            if not course:
                return {
                    "error": f"Student with id {student_id} is not assigned to course with id {course_id}"
                }, HTTPStatus.NOT_FOUND
            else:
                student_course_repository.delete_course_to_student_by_id(course)
            return {
                "message": f"Course by id {course_id} has been deleted from student with id {student_id}."
            }, HTTPStatus.OK


class CourseStudentListAPI(MethodResource, Resource):
    @doc(description="Get all students in the course", tags=["Courses"])
    @marshal_with(CourseNotFoundSchema, code=404)
    @marshal_with(StudentResponseSchema(many=True), code=200)
    def get(self, course_id) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            course = course_repository.get_course_by_id(course_id)
            if not course:
                return {
                    "error": f"Course by id {course_id} not found."
                }, HTTPStatus.NOT_FOUND
            students = StudentRepository(session).get_students_related_to_course(
                course_id
            )
            dict_students = list(
                map(
                    lambda student: asdict(StudentDataclass.from_sqlalchemy(student)),
                    students,
                )
            )
            return dict_students, HTTPStatus.OK

    @doc(description="Add a student to the course", tags=["Courses"])
    @use_kwargs(StudentsIdSchema)
    @marshal_with(CourseNotFoundSchema, code=404)
    @marshal_with(AddCourseStudentRequestSchema, code=200)
    def post(self, course_id, **kwargs) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            course = course_repository.get_course_by_id(course_id)
            if not course:
                return {
                    "error": f"Course by id {course_id} not found."
                }, HTTPStatus.NOT_FOUND
            student_repository = StudentRepository(session)
            student = student_repository.get_student_by_id(kwargs["student_id"])
            if not student:
                return {
                    "error": f"This student by id  {kwargs['student_id']} is not exists."
                }, HTTPStatus.NOT_FOUND

            student_course_repository = StudentCourseRepository(session)
            course_of_student = student_course_repository.get_students_course(
                kwargs["student_id"], course_id
            )

            if course_of_student:
                return {
                    "error": f"Student with id {kwargs['student_id']} is already assigned to course with id {course_id}."
                }, HTTPStatus.NOT_FOUND

            else:
                student_course_repository.add_student_to_course(
                    kwargs["student_id"], course_id
                )
                return {"message": "Сourse has been successfully added"}, HTTPStatus.OK


class CoursesListApi(MethodResource, Resource):
    @doc(description="Get all courses", tags=["Courses"])
    @marshal_with(CourseResponseSchema(many=True), code=200)
    def get(self) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            courses = course_repository.get_all_courses()
            dict_courses = list(
                map(
                    lambda course: asdict(CourseDataclass.from_sqlalchemy(course)),
                    courses,
                )
            )
            return dict_courses, HTTPStatus.OK

    @doc(description="Create new course", tags=["Courses"])
    @use_kwargs(CourseRequestSchema)
    @marshal_with(AddCourseRequestSchema, code=200)
    def post(self, **kwargs) -> wrappers.Response:
        with get_session() as session:
            course_repository = CourseRepository(session)
            course_repository.create_course(kwargs["name"])
            return {
                "message": f"Course with name {kwargs['name']} was created successfully."
            }, HTTPStatus.OK


class CourseApi(MethodResource, Resource):
    @doc(description="Get course by id", tags=["Courses"])
    @marshal_with(CourseResponseSchema, code=200)
    @marshal_with(CourseNotFoundSchema, code=404)
    def get(self, course_id):
        with get_session() as session:
            course_repository = CourseRepository(session)
            course = course_repository.get_course_by_id(course_id)
            if not course:
                return {
                    "error": f"Course with {course_id} not found."
                }, HTTPStatus.NOT_FOUND
            return asdict(CourseDataclass.from_sqlalchemy(course)), HTTPStatus.OK

    @doc(description="Delete course by id", tags=["Courses"])
    @marshal_with(DeleteCourseSchema, code=200)
    @marshal_with(CourseNotFoundSchema, code=404)
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
