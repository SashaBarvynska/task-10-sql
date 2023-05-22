from sqlalchemy import func

from src.database import GroupModel, StudentModel

from .base_repository import BaseReporistory


class GroupRepository(BaseReporistory):
    def get_groups_with_max_students(self, max_students: int) -> list[GroupModel]:
        return self.session.query(GroupModel).join(StudentModel, StudentModel.group_id == GroupModel.id).group_by(
            GroupModel.id
        ).having(func.count(StudentModel.id) <= max_students).all()
