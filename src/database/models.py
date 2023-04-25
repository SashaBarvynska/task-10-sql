from peewee import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.connection import Base

# from sqlalchemy.orm import relationship, backref


class GroupModel(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("GroupModel", backref="students")


class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    student = relationship("StudentModel", secondary="student_course", backref="courses")


class StudentCourseModel(Base):
    __tablename__ = 'student_course'
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), primary_key=True)
    course_id = (Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True))


MODELS: list[Model] = [GroupModel, StudentModel, CourseModel, StudentCourseModel]
