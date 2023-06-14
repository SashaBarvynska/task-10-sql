from src.api.students import StudentsListApi, StudentApi
from src.api.groups import GroupsListApi, GroupApi
from src.api.courses import (
    CourseApi,
    CoursesListApi,
    CourseStudentApi,
    CourseStudentListAPI,
)
from flask import Flask

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


def init_swagger(app: Flask):
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="task 10 SQL",
                version="v1",
                plugins=[MarshmallowPlugin()],
                openapi_version="2.0.0",
            ),
            "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
            "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
        }
    )
    docs = FlaskApiSpec(app)

    docs.register(StudentsListApi)
    docs.register(StudentApi)
    docs.register(GroupsListApi)
    docs.register(GroupApi)
    docs.register(CourseApi)
    docs.register(CoursesListApi)
    docs.register(CourseStudentApi)
    docs.register(CourseStudentListAPI)
