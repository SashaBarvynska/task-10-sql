from flask_restful import Resource
from flask import Flask, request
from http import HTTPStatus
from flask import wrappers
from src.database.repositories import StudentRepository
from src.database.connection import get_session
from flask_restful import Api
from dataclasses import asdict
from src.dataclass import Student


class StudentsListAPI(Resource):
    def post(self):
        with get_session() as session:
            data = request.get_json()
            new_student = StudentRepository(session).create_student(data)
            student = Student(
                new_student.id, new_student.first_name, new_student.last_name
            )
            return asdict(student), HTTPStatus.OK

    def get(self) -> wrappers.Response:
        with get_session() as session:
            student_repository = StudentRepository(session)
            students = student_repository.get_all_students()
            dict_students = list(
                map(
                    lambda student: asdict(
                        Student(student.id, student.first_name, student.last_name)
                    ),
                    students,
                )
            )
            return dict_students, HTTPStatus.OK


class StudentAPI(Resource):
    def get(self, student_id: int) -> wrappers.Response:
        with get_session() as session:
            student_repository = StudentRepository(session)
            student = student_repository.get_student_by_id(student_id)
            formated_student = Student(
                student.id, student.first_name, student.last_name
            )
            return asdict(formated_student), HTTPStatus.OK

    def delete(self, student_id: int) -> wrappers.Response:
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

    def patch(self, student_id: int):
        with get_session() as session:
            data = request.get_json()
            student_repository = StudentRepository(session)
            student = student_repository.get_student_by_id(student_id)
            if "first_name" in data:
                student.first_name = data["first_name"]
            if "last_name" in data:
                student.last_name = data["last_name"]
