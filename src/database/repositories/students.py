from typing import List, TypedDict

from src.database.models import (
    CourseModel,
    StudentCourseModel,
    StudentModel,
    GroupModel,
)

from .base_repository import BaseRepository


class CreateStudent(TypedDict):
    first_name: str
    last_name: str


class StudentRepository(BaseRepository):
    def create_student(self, data: CreateStudent) -> StudentModel:
        student = StudentModel(
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

        self.session.add(student)
        self.session.flush()
        return student

    def get_student_by_id(self, student_id: int) -> StudentModel or None:
        return (
            self.session.query(StudentModel)
            .filter(StudentModel.id == student_id)
            .first()
        )

    def delete_student_by_id(self, student_id: int) -> None:
        self.session.query(StudentModel).filter(StudentModel.id == student_id).delete()

    def get_students_related_to_course(self, course_id: int) -> List[StudentModel]:
        return (
            self.session.query(StudentModel)
            .join(StudentCourseModel)
            .join(CourseModel)
            .filter(CourseModel.id == course_id)
            .all()
        )

    def get_all_students(self) -> list[StudentModel]:
        return self.session.query(StudentModel).all()

    def get_students_by_group_id(self, group_id) -> list[StudentModel]:
        return (
            self.session.query(StudentModel)
            .join(GroupModel)
            .filter(GroupModel.id == group_id)
            .all()
        )
