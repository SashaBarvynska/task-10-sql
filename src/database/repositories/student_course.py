from typing import List

from src.database.models import CourseModel, StudentCourseModel, StudentModel

from .base_repository import BaseRepository


class StudentCourseRepository(BaseRepository):
    def get_students_course(self, student_id: int, course_id: int) -> List[int]:
        return (
            self.session.query(StudentCourseModel.course_id)
            .filter(
                StudentCourseModel.student_id == student_id,
                StudentCourseModel.course_id == course_id,
            )
            .first()
        )

    def get_course_to_student_by_id(
        self, course_id: int, student_id: int
    ) -> StudentCourseModel | None:
        return (
            self.session.query(StudentCourseModel)
            .filter(
                StudentCourseModel.student_id == student_id,
                StudentCourseModel.course_id == course_id,
            )
            .first()
        )

    def delete_course_to_student_by_id(self, student_id: int) -> None:
        self.session.delete(student_id)

    def add_student_to_course(self, student_id: int, course_id: int) -> None:
        add_course_id = StudentCourseModel(student_id=student_id, course_id=course_id)
        self.session.add(add_course_id)
