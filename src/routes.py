from dataclasses import asdict, dataclass
from http import HTTPStatus

from flask import request, wrappers

from src import (GroupRepository, StudentCourseRepository, StudentRepository,
                 get_session)
from src.app import app


@dataclass
class Student:
    id: int
    first_name: str
    last_name: str


@dataclass
class Group:
    id: int
    name: str


# Add new student
@app.route('/students', methods=['POST'])
def add_student() -> wrappers.Response:
    with get_session() as session:
        data = request.get_json()
        new_student = StudentRepository.create_student(session, data)
        student = Student(new_student.id, new_student.first_name, new_student.last_name)
        return asdict(student), HTTPStatus.OK


# Delete student by STUDENT_ID
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id: int) -> wrappers.Response:
    with get_session() as session:
        student = StudentRepository.get_student_by_id(session, id)
        if not student:
            return {'error': 'Student by {id} not found.'}, HTTPStatus.NOT_FOUND
        else:
            StudentRepository.delete_student_by_id(session, id)
            return {'message': f'Student by {id} has been deleted.'}, HTTPStatus.OK


# Find all students related to the course with a given name.
@app.route('/students', methods=['GET'])
def get_courses() -> wrappers.Response:
    with get_session() as session:
        course = request.args.get('course')
        students = StudentRepository.get_students_related_to_course(session, course)
        dict_students = list(map(lambda student: asdict(
            Student(student.id, student.first_name, student.last_name)
            ), students))
        return dict_students, HTTPStatus.OK


# Add a student to the course (from a list)
@app.route('/students/add_course', methods=['POST'])
def add_student_to_course() -> wrappers.Response:
    with get_session() as session:
        data = request.get_json()
        course_id = StudentCourseRepository.get_an_existing_course_from_the_student(session, data)
        if course_id:
            return {'error': f'this course by id {[q[0] for q in course_id]} already exists'}, HTTPStatus.NOT_FOUND
        else:
            for id in data['course_id']:
                StudentCourseRepository.add_student_to_course(session, data, id)
            return {'massage': "course was added successfully"}, HTTPStatus.OK


# Remove the student from one of his or her courses
@app.route('/students/<int:id>/courses', methods=['DELETE'])
def delete_course(id: int) -> wrappers.Response:
    with get_session() as session:
        course_id = request.args.get('course')
        course = StudentCourseRepository.get_course_to_student_by_id(session, course_id, id)
        if not course:
            return {'error': f'Course by id {course.course_id} not found.'}, HTTPStatus.NOT_FOUND
        else:
            StudentCourseRepository.delete_course_to_student_by_id(session, course)
        return {'message': f'Course by id {course.course_id} has been deleted.'}, HTTPStatus.OK


# Find all groups with less or equals student count.
@app.route('/groups', methods=['GET'])
def get_groups() -> wrappers.Response:
    with get_session() as session:
        max_students = request.args.get('max_students')
        dict_students = list(map(lambda group: asdict(
            Group(group.id, group.name)
            ), GroupRepository.get_groups_with_max_students(session, max_students)))
        return dict_students, HTTPStatus.OK


@app.errorhandler(404)
def handle_exception(e) -> wrappers.Response:
    return {"message": "Page Not Found"}, HTTPStatus.NOT_FOUND
