from flask_restful import Resource

from http import HTTPStatus
from src.database.repositories import GroupRepository, StudentRepository
from src.database.connection import get_session
from flask import wrappers
from dataclasses import asdict
from src.api.dataclass import GroupDataclass
from flask_restful import Resource
from flask import wrappers
from dataclasses import asdict
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from src.swagger.groups import (
    GroupResponseSchema,
    GroupRequestSchema,
    DeleteGroupSchema,
    GroupNotFoundSchema,
)
from marshmallow import fields


class GroupsListApi(MethodResource, Resource):
    @doc(
        description="Get all groups or get groups with filtering by the maximum number of students",
        tags=["Groups"],
    )
    @use_kwargs(
        {"max_students": fields.Int(example=15)},
        location="query",
    )
    @marshal_with(GroupResponseSchema(many=True), code=200)
    def get(self, max_students: int | None = None) -> wrappers.Response:
        with get_session() as session:
            groups_repository = GroupRepository(session)
            groups = groups_repository.get_groups(max_students)
            dict_groups = list(
                map(
                    lambda group: asdict(GroupDataclass.from_sqlalchemy(group)),
                    groups,
                )
            )
            return dict_groups, HTTPStatus.OK

    @doc(
        description="Create new group",
        tags=["Groups"],
    )
    @use_kwargs(GroupRequestSchema)
    @marshal_with(GroupResponseSchema, code=200)
    def post(self, name_group):
        with get_session() as session:
            new_group = GroupRepository(session).create_group(name_group)
            return asdict(GroupDataclass.from_sqlalchemy(new_group)), HTTPStatus.OK


class GroupApi(MethodResource, Resource):
    @doc(description="Delete group by id", tags=["Groups"])
    @marshal_with(DeleteGroupSchema, code=200)
    @marshal_with(GroupNotFoundSchema, code=404)
    def delete(self, group_id: int) -> wrappers.Response:
        with get_session() as session:
            group_repository = GroupRepository(session)
            group = group_repository.get_group_by_id(group_id)
            if not group:
                return {
                    "error": f"Group with id {group_id} not found."
                }, HTTPStatus.NOT_FOUND
            else:
                student_repository = StudentRepository(session)
                students = student_repository.get_students_by_group_id(group_id)
                for student in students:
                    student.group_id = None
                group_repository.delete_group_by_id(group_id)
                return {
                    "message": f"Group with id {group_id} has been deleted."
                }, HTTPStatus.OK

    @doc(description="Get group by id", tags=["Groups"])
    @marshal_with(GroupResponseSchema, code=200)
    @marshal_with(GroupNotFoundSchema, code=404)
    def get(self, group_id: int) -> wrappers.Response:
        with get_session() as session:
            group_repository = GroupRepository(session)
            group = group_repository.get_group_by_id(group_id)
            if not group:
                return {
                    "error": f"Group with {group_id} not found."
                }, HTTPStatus.NOT_FOUND
            return asdict(GroupDataclass.from_sqlalchemy(group)), HTTPStatus.OK
