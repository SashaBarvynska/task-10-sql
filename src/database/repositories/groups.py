from sqlalchemy import func

from src.database.models import GroupModel, StudentModel
from .base_repository import BaseRepository


class GroupRepository(BaseRepository):
    def get_groups(self, max_students: int | None = None):
        query = self.session.query(GroupModel)
        if max_students:
            query = (
                query.join(StudentModel)
                .filter(GroupModel.id == StudentModel.group_id)
                .group_by(GroupModel.id)
                .having(func.count(StudentModel.id) <= max_students)
            )
        return query.all()

    def create_group(self, name_group: str) -> GroupModel:
        group = GroupModel(name=name_group)
        self.session.add(group)
        self.session.flush()
        return group

    def get_group_by_id(self, group_id: int) -> GroupModel or None:
        return self.session.query(GroupModel).filter(GroupModel.id == group_id).first()

    def delete_group_by_id(self, group_id: int) -> None:
        self.session.query(GroupModel).filter(GroupModel.id == group_id).delete()
