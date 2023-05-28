from dataclasses import asdict
from http import HTTPStatus
from src.dataclass import Student, Group
import jsonpickle

from flasgger import swag_from
from flask import request, wrappers

from src import (
    GroupRepository,
    StudentCourseRepository,
    StudentRepository,
    get_session,
    StudentModel,
)
from src.app import app


# Add new student
@app.route("/students", methods=["POST"])
@swag_from("swagger/students.yml")
def add_student() -> wrappers.Response:
    with get_session() as session:
        data = request.get_json()
        new_student = StudentRepository(session).create_student(data)
        student = Student(new_student.id, new_student.first_name, new_student.last_name)
        return asdict(student), HTTPStatus.OK


# Delete student by STUDENT_ID
@app.route("/students/<int:student_id>", methods=["DELETE"])
@swag_from("swagger/students.yml")
def delete_student(student_id: int) -> wrappers.Response:
    with get_session() as session:
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(student_id)
        if not student:
            return {
                "error": f"Student by {student_id} not found."
            }, HTTPStatus.NOT_FOUND
        else:
            student_repository.delete_student_by_id(student_id)
            return {
                "message": f"Student by {student_id} has been deleted."
            }, HTTPStatus.OK


# Find all students related to the course with a given name.
@app.route("/students", methods=["GET"])
@swag_from("swagger/students.yml")
def get_courses():
    with get_session() as session:
        course = request.args.get("course")
        students = StudentRepository(session).get_students_related_to_course(course)
        dict_students = list(
            map(
                lambda student: asdict(
                    Student(student.id, student.first_name, student.last_name)
                ),
                students,
            )
        )
        return jsonpickle.encode(dict_students), HTTPStatus.OK


# Add a student to the course (from a list)
@app.route("/students/add_course", methods=["POST"])
@swag_from("swagger/courses.yml")
def add_student_to_course() -> wrappers.Response:
    with get_session() as session:
        data = request.get_json()
        student_course_repository = StudentCourseRepository(session)
        course_id = student_course_repository.get_an_existing_course_from_the_student(
            data
        )
        if course_id:
            return {
                "error": f"This course by id {[q[0] for q in course_id]} already exists."
            }, HTTPStatus.NOT_FOUND
        else:
            for course_id in data["course_id"]:
                student_course_repository.add_student_to_course(data, course_id)
            return {"message": "Course was added successfully."}, HTTPStatus.OK


# Remove the student from one of his or her courses
@app.route("/students/<int:student_id>/courses", methods=["DELETE"])
@swag_from("swagger/courses.yml")
def delete_course(student_id: int) -> wrappers.Response:
    with get_session() as session:
        course_id = request.args.get("course")
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


# Find all groups with less or equals student count.
@app.route("/groups", methods=["GET"])
@swag_from("swagger/groups.yml")
def get_groups() -> wrappers.Response:
    with get_session() as session:
        max_students = request.args.get("max_students")
        groups_with_max_students = GroupRepository(
            session
        ).get_groups_with_max_students(max_students)
        dict_students = list(
            map(
                lambda group: asdict(Group(group.id, group.name)),
                groups_with_max_students,
            )
        )
        return jsonpickle.encode(dict_students), HTTPStatus.OK


@app.errorhandler(404)
def handle_exception(e) -> wrappers.Response:
    return {"message": "Page Not Found."}, HTTPStatus.NOT_FOUND
