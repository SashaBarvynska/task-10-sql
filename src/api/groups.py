from flask_restful import Resource

from flask import request
from http import HTTPStatus
from src.database.repositories import GroupRepository, StudentRepository
from src.database.connection import get_session
from flask import wrappers
from dataclasses import asdict
from src.api.dataclass import Group


class GroupsListApi(Resource):
    #  get all groups
    def get(self) -> wrappers.Response:
        with get_session() as session:
            max_students = request.args.get("max_students")
            groups_repository = GroupRepository(session)
            groups = groups_repository.get_groups(max_students)
            dict_groups = list(
                map(
                    lambda group: asdict(Group(group.id, group.name)),
                    groups,
                )
            )
            return dict_groups, HTTPStatus.OK

    def post(self):
        with get_session() as session:
            data = request.get_json()
            name_group = data["name"]
            new_group = GroupRepository(session).create_group(name_group)
            formatted_group = Group(new_group.id, new_group.name)
            return asdict(formatted_group), HTTPStatus.OK


class GroupApi(Resource):
    #  delete group by id
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

    def get(self, group_id: int) -> wrappers.Response:
        with get_session() as session:
            group_repository = GroupRepository(session)
            group = group_repository.get_group_by_id(group_id)
            formated_group = Group(group.id, group.name)
            return asdict(formated_group), HTTPStatus.OK
