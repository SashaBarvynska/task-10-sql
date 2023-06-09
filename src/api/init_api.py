from flask import Flask

from flask_restful import Api
from src.api.students import StudentApi, StudentsListApi
from src.api.courses import (
    CourseStudentListAPI,
    CourseStudentApi,
    CoursesListApi,
    CourseApi,
)
from src.api.groups import GroupsListApi, GroupApi


def init_api(app: Flask):
    api = Api(app)

    # students
    api.add_resource(StudentsListApi, "/students")
    api.add_resource(StudentApi, "/students/<int:student_id>")

    # students by course
    api.add_resource(CourseStudentListAPI, "/courses/<int:course_id>/students")
    api.add_resource(
        CourseStudentApi, "/courses/<int:course_id>/students/<int:student_id>"
    )

    # courses
    api.add_resource(CoursesListApi, "/courses")
    api.add_resource(CourseApi, "/courses/<int:course_id>")

    # groups
    api.add_resource(GroupsListApi, "/groups")
    api.add_resource(GroupApi, "/groups/<int:group_id>")
