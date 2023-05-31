from typing import List, TypedDict

from src.database.models import CourseModel, StudentCourseModel, StudentModel

from .base_repository import BaseRepository


class GetIdsStudentAndCourse(TypedDict):
    student_id: int
    course_id: int


class StudentCourseRepository(BaseRepository):
    def add_course_id(student_id: int, course_id: int) -> StudentCourseModel:
        return StudentCourseModel(student_id=student_id, course_id=course_id)

    def get_an_existing_course_from_the_student(
        self, data: GetIdsStudentAndCourse
    ) -> List[int]:
        return (
            self.session.query(CourseModel.id)
            .join(StudentCourseModel, CourseModel.id == StudentCourseModel.course_id)
            .join(StudentModel, StudentModel.id == StudentCourseModel.student_id)
            .filter(
                StudentModel.id == data["student_id"],
                CourseModel.id.in_(data["course_id"]),
            )
            .all()
        )

    def get_course_to_student_by_id(
        self, course_id: int, student_id: int
    ) -> StudentCourseModel | None:
        return (
            self.session.query(StudentCourseModel)
            .join(CourseModel, CourseModel.id == StudentCourseModel.course_id)
            .join(StudentModel, StudentModel.id == StudentCourseModel.student_id)
            .filter(StudentModel.id == student_id, CourseModel.id == course_id)
            .first()
        )

    def delete_course_to_student_by_id(self, student_id: int) -> None:
        self.session.delete(student_id)

    def add_student_to_course(
        self, data: GetIdsStudentAndCourse, course_id: int
    ) -> None:
        add_course_id = StudentCourseModel(
            student_id=data["student_id"], course_id=course_id
        )
        self.session.add(add_course_id)
