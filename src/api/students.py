from flask_restful import Resource
from flask import wrappers
from http import HTTPStatus
from src.database.repositories import StudentRepository
from src.database.connection import get_session
from dataclasses import asdict
from src.api.dataclass import StudentDataclass
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from src.swagger.students import (
    StudentNotFoundSchema,
    StudentRequestSchema,
    StudentResponseSchema,
    PatchStudentSchema,
    DeleteStudentSchema,
)


class StudentsListApi(MethodResource, Resource):
    @doc(description="Create new student", tags=["Students"])
    @use_kwargs(StudentRequestSchema)
    @marshal_with(StudentResponseSchema, code=200)
    def post(self, **kwargs):
        with get_session() as session:
            new_student = StudentRepository(session).create_student(kwargs)
            return (
                asdict(StudentDataclass.from_sqlalchemy(new_student)),
                HTTPStatus.OK,
            )

    @doc(description="Get all students", tags=["Students"])
    @marshal_with(StudentResponseSchema(many=True), code=200)
    def get(self) -> wrappers.Response:
        with get_session() as session:
            student_repository = StudentRepository(session)
            students = student_repository.get_all_students()
            dict_students = list(
                map(
                    lambda student: asdict(StudentDataclass.from_sqlalchemy(student)),
                    students,
                )
            )
            return dict_students, HTTPStatus.OK


class StudentApi(MethodResource, Resource):
    @doc(description="Get student by id", tags=["Students"])
    @marshal_with(StudentResponseSchema, code=200)
    @marshal_with(StudentNotFoundSchema, code=404)
    def get(self, student_id: int) -> wrappers.Response:
        with get_session() as session:
            student_repository = StudentRepository(session)
            student = student_repository.get_student_by_id(student_id)
            if not student:
                return {
                    "error": f"Student by {student_id} not found."
                }, HTTPStatus.NOT_FOUND
            return asdict(StudentDataclass.from_sqlalchemy(student)), HTTPStatus.OK

    @doc(description="Delete student by id", tags=["Students"])
    @marshal_with(DeleteStudentSchema, code=200)
    @marshal_with(StudentNotFoundSchema, code=404)
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

    @doc(description="Update student", tags=["Students"])
    @use_kwargs(StudentRequestSchema)
    @marshal_with(PatchStudentSchema, code=200)
    @marshal_with(StudentNotFoundSchema, code=404)
    def patch(self, **kwargs: int):
        with get_session() as session:
            student_repository = StudentRepository(session)
            student = student_repository.get_student_by_id(kwargs["student_id"])
            if not student:
                return {
                    "error": f"Student by {kwargs['student_id']} not found."
                }, HTTPStatus.NOT_FOUND

            else:
                student_repository.patch_student(student, kwargs)
                return (
                    {"message": f"Student by {kwargs['student_id']} has been updated."},
                    HTTPStatus.OK,
                )
