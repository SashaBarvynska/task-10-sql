from typing import List, TypedDict

from sqlalchemy.orm import Session

from src.database import CourseModel, StudentCourseModel, StudentModel


class CreateStudent(TypedDict):
    first_name: str
    last_name: str


class StudentRepository:
    def create_student(session: Session, data: CreateStudent) -> StudentModel:
        student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        session.add(student)
        return student

    def get_student_by_id(session: Session, id: int) -> StudentModel or None:
        return session.query(StudentModel).filter_by(id=id).first()

    def delete_student_by_id(session: Session, id: int):
        session.query(StudentModel).filter_by(id=id).delete()

    def get_students_related_to_course(session: Session, name_course: str) -> List[StudentModel]:
        return session.query(StudentModel).join(StudentCourseModel).join(CourseModel).filter(
            CourseModel.name == name_course).all()

    def get_all_students(session: Session) -> list[StudentModel]:
        return session.query(StudentModel)
