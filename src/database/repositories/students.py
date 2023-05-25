from typing import List, TypedDict

from src.database import CourseModel, StudentCourseModel, StudentModel

from .base_repository import BaseReporistory


class CreateStudent(TypedDict):
    first_name: str
    last_name: str


class StudentRepository(BaseReporistory):
    def create_student(self, **data: CreateStudent) -> StudentModel:
        student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        self.session.add(student)
        self.session.flush()
        return student

    def get_student_by_id(self, student_id: int) -> StudentModel or None:
        return self.session.query(StudentModel).filter(StudentModel.id == student_id).first()

    def delete_student_by_id(self, student_id: int) -> None:
        self.session.query(StudentModel).filter(StudentModel.id == student_id).delete()

    def get_students_related_to_course(self, name_course: str) -> List[StudentModel]:
        return self.session.query(StudentModel.id).join(StudentCourseModel).join(CourseModel).filter(
            CourseModel.name == name_course).all()

    def get_all_students(self) -> list[StudentModel]:
        return self.session.query(StudentModel).all()
