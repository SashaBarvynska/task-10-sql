from typing import List, TypedDict

from src.database import CourseModel, StudentCourseModel, StudentModel

from .base_repository import BaseReporistory


class GetIdsStudentAndCourse(TypedDict):
    student_id: int
    course_id: int


class StudentCourseRepository(BaseReporistory):
    def add_course_id(student_id: int, id: int) -> StudentCourseModel:
        return StudentCourseModel(student_id=student_id, course_id=id)

    def get_an_existing_course_from_the_student(self, data: GetIdsStudentAndCourse) -> List[int]:
        return self.session.query(CourseModel.id).join(StudentCourseModel).join(StudentModel).filter(
            StudentModel.id == data['student_id'], CourseModel.id.in_(data['course_id'])
            ).all()

    def get_course_to_student_by_id(self, course: int, id: int) -> StudentCourseModel | None:
        return self.session.query(StudentCourseModel).join(CourseModel).join(StudentModel).filter(
            StudentModel.id == id, CourseModel.id == course
            ).first()

    def delete_course_to_student_by_id(self, id: int) -> None:
        self.session.delete(id)

    def add_student_to_course(self, data: GetIdsStudentAndCourse, id: int) -> None:
        add_course_id = StudentCourseModel(student_id=data['student_id'], course_id=id)
        self.session.add(add_course_id)
