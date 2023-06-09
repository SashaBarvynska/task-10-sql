from src.database.models import CourseModel

from .base_repository import BaseRepository


class CourseRepository(BaseRepository):
    def get_all_courses(self):
        return self.session.query(CourseModel).all()

    def create_course(self, course_name):
        course = CourseModel(name=course_name)
        self.session.add(course)
        self.session.flush()
        return course

    def get_course_by_id(self, course_id: int) -> CourseModel or None:
        return (
            self.session.query(CourseModel).filter(CourseModel.id == course_id).first()
        )

    def delete_course_by_id(self, course_id: int) -> None:
        self.session.query(CourseModel).filter(CourseModel.id == course_id).delete()
