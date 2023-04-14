from peewee import Model
from sqlalchemy import Column, ForeignKey, Integer, String

from src.database.connection import Base


class GroupModel(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True)
    name = Column(String)


class StudentModel(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'))


class CourseModel(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class StudentCourseModel(Base):
    __tablename__ = 'student_course'
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), primary_key=True)


MODELS: list[Model] = [GroupModel, StudentModel, CourseModel, StudentCourseModel]
