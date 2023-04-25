from typing import List, TypedDict

from sqlalchemy.orm import Session

from src.database import CourseModel, StudentCourseModel, StudentModel


class GetIdsStudentAndCourse(TypedDict):
    student_id: int
    course_id: int


class StudentCourseRepository:
    def add_course_id(student_id: int, id: int) -> StudentCourseModel:
        return StudentCourseModel(student_id=student_id, course_id=id)

    def get_an_existing_course_from_the_student(session: Session, data: GetIdsStudentAndCourse) -> List[(int)]:
        return session.query(CourseModel.id).join(StudentCourseModel).join(StudentModel).filter(
            StudentModel.id == data['student_id'], CourseModel.id.in_(data['course_id'])
            ).all()

    def get_course_to_student_by_id(session: Session, course: int, id: int) -> (StudentCourseModel | None):
        return session.query(StudentCourseModel).join(CourseModel).join(StudentModel).filter(
            StudentModel.id == id, CourseModel.id == course
            ).first()

    def delete_course_to_student_by_id(session: Session, id: int) -> None:
        session.delete(id)

    def add_student_to_course(session: Session, data: GetIdsStudentAndCourse, id: int) -> None:
        add_course_id = StudentCourseModel(student_id=data['student_id'], course_id=id)
        session.add(add_course_id)
