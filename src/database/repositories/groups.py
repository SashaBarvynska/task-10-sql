from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database import GroupModel, StudentModel


class GroupRepository:
    def get_groups_with_max_students(session: Session, max_students: int) -> list[GroupModel]:
        return session.query(GroupModel).join(StudentModel).group_by(
            GroupModel.id
        ).having(func.count(StudentModel.id) <= max_students).all()
