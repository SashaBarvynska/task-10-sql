from typing import List, TypedDict

from src.database.models import CourseModel, StudentModel, StudentCourseModel

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

    def patch_student(self, student: StudentModel, kwargs: dict[str, str]) -> None:
        student.first_name = kwargs["first_name"]
        student.last_name = kwargs["last_name"]

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
            .filter(StudentCourseModel.course_id == course_id)
            .all()
        )

    def get_all_students(self) -> list[StudentModel]:
        return self.session.query(StudentModel).all()

    def get_students_by_group_id(self, group_id) -> list[StudentModel]:
        return (
            self.session.query(StudentModel)
            .filter(StudentModel.group_id == group_id)
            .all()
        )
