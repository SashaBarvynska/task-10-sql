from peewee import Model
from sqlalchemy import ForeignKey, Integer, String

from src.database.connection import db


class GroupModel(db.Model):
    __tablename__ = "groups"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)


class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String, nullable=False)
    last_name = db.Column(String, nullable=False)
    group_id = db.Column(Integer, ForeignKey("groups.id"))
    group = db.relationship("GroupModel", backref="students")


class CourseModel(db.Model):
    __tablename__ = "courses"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    description = db.Column(String)
    student = db.relationship(
        "StudentModel", secondary="student_course", backref="courses"
    )


class StudentCourseModel(db.Model):
    __tablename__ = "student_course"
    student_id = db.Column(
        Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True
    )
    course_id = db.Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True
    )


MODELS: list[Model] = [GroupModel, StudentModel, CourseModel, StudentCourseModel]
