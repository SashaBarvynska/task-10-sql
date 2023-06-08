from flask import Flask

from flask_restful import Api
from src.api.students import StudentAPI, StudentsListAPI


def init_api(app: Flask):
    api = Api(app)
    api.add_resource(StudentsListAPI, "/students")
    api.add_resource(StudentAPI, "/students/<int:student_id>")
